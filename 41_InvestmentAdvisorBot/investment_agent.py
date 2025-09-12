import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

import openai

from config import get_api_key


class InvestmentAdvisor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        if not self.api_key:
            # allow running in offline/mock mode
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=self.api_key)

    def build_prompt(self, profile: Dict[str, Any]) -> str:
        prompt = (
            "You are InvestmentAdvisorBot, a friendly financial advisor that provides educational, simulated advice. "
            "Do not provide investment execution instructions or financial services. Use the user profile to recommend a simple allocation plan and explanations.\n\n"
        )
        prompt += "User profile:\n"
        for k, v in profile.items():
            prompt += f"- {k}: {v}\n"

        prompt += (
            "\nRespond in Markdown only with sections: ## Financial Summary, ## Investment Plan, ## Diversification Strategy, ## Recommendations. "
            "Include a JSON block at the end named allocation with asset classes and percentages. Keep it concise and beginner-friendly."
        )
        return prompt

    def generate_advice(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate advice using OpenAI or a local heuristic when API key is missing."""
        prompt = self.build_prompt(profile)

        if not self.client:
            # Mock heuristic fallback
            allocation = self.heuristic_allocation(profile)
            md = self.heuristic_markdown(profile, allocation)
            return {"markdown": md, "allocation": allocation}

        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are InvestmentAdvisorBot."},
                          {"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800,
            )
            content = resp.choices[0].message.content
            # Attempt to extract JSON allocation if present
            allocation = self.extract_allocation_from_text(content)
            return {"markdown": content, "allocation": allocation}
        except Exception as e:
            # On error, return heuristic
            allocation = self.heuristic_allocation(profile)
            md = self.heuristic_markdown(profile, allocation)
            return {"markdown": md, "allocation": allocation, "error": str(e)}

    def extract_allocation_from_text(self, text: str) -> Dict[str, Any]:
        # naive extraction: look for a JSON block
        import re
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return {}
        try:
            return json.loads(m.group(0))
        except Exception:
            return {}

    def heuristic_allocation(self, profile: Dict[str, Any]) -> Dict[str, float]:
        # Simple rule-based allocation
        risk = profile.get("risk", "medium").lower()
        age = int(profile.get("age", 30))
        goal = profile.get("goal", "long-term").lower()

        if risk == "low":
            allocation = {"bonds": 50, "mutual_funds": 30, "stocks": 10, "gold": 5, "cash": 5}
        elif risk == "high":
            allocation = {"stocks": 60, "crypto": 15, "mutual_funds": 15, "gold": 5, "cash": 5}
        else:
            allocation = {"mutual_funds": 50, "stocks": 30, "bonds": 10, "gold": 5, "cash": 5}

        # small age-based tweak: younger -> more stocks
        if age < 30 and risk != "low":
            allocation["stocks"] = allocation.get("stocks", 0) + 10
            if allocation.get("bonds"):
                allocation["bonds"] = max(0, allocation["bonds"] - 10)

        # Normalize to 100
        total = sum(allocation.values())
        for k in allocation:
            allocation[k] = round((allocation[k] / total) * 100, 1)

        return allocation

    def heuristic_markdown(self, profile: Dict[str, Any], allocation: Dict[str, float]) -> str:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        lines = []
        lines.append(f"## Financial Summary\n\n")
        lines.append(f"- Generated: {now}\n")
        lines.append(f"- Monthly income: {profile.get('income')}")
        lines.append(f"- Age: {profile.get('age')}")
        lines.append(f"- Risk appetite: {profile.get('risk')}")
        lines.append(f"- Goal: {profile.get('goal')}\n\n")

        lines.append("## Investment Plan\n\n")
        save_pct = profile.get('save_pct') or self.recommend_save_pct(profile)
        lines.append(f"- Suggested savings: **{save_pct}%** of monthly income\n\n")

        lines.append("## Suggested Allocation\n\n")
        for k, v in allocation.items():
            lines.append(f"- **{k.title().replace('_', ' ')}**: {v}%")
        lines.append("\n")

        lines.append("## Why This Plan Fits You\n\n")
        lines.append("A balanced, diversified allocation based on your risk profile and age. Adjust periodically and consult a certified advisor for decisions involving real money.")

        # add JSON block
        lines.append("\n```json\n")
        lines.append(json.dumps(allocation, indent=2))
        lines.append("\n```\n")

        return "\n".join(lines)

    def recommend_save_pct(self, profile: Dict[str, Any]) -> int:
        income = float(profile.get('income', 0))
        risk = profile.get('risk', 'medium').lower()
        if income <= 500:
            return 10
        if risk == 'high':
            return 20
        if risk == 'low':
            return 15
        return 15

    def export_markdown(self, markdown: str, path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(markdown)

    def export_json(self, data: Dict[str, Any], path: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
import json
from typing import Dict, Any, Optional
import openai
from config import Config


class InvestmentAdvisorBot:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.get_api_key()
        if not self.api_key:
            raise ValueError("OpenAI API key not set. Call Config.setup_instructions().")
        self.client = openai.OpenAI(api_key=self.api_key)

    def build_prompt(self, profile: Dict[str, Any]) -> str:
        # Compose system + user prompt to instruct the model to produce markdown output
        system = (
            "You are InvestmentAdvisorBot, a helpful financial-advice assistant. "
            "Provide educational, non-professional suggestions only."
        )

        user = (
            "Given the following user profile, return a markdown-formatted investment plan. "
            "Include sections: ## Financial Summary, ## Investment Plan, ## Diversification Strategy, "
            "## Recommendations. Also output a JSON object at the end enclosed in triple backticks with key 'allocation' describing percentages for asset classes.\n\n"
            f"Profile:\n{json.dumps(profile, indent=2)}\n\n"
            "Rules:\n"
            "- Suggest a saving percentage and explain why.\n"
            "- Suggest allocations across 4-6 asset classes.\n"
            "- Make the plan appropriate to age, income, risk level, and goal.\n"
            "- Do not provide legal/financial compliance advice.\n"
            "- Keep language simple and beginner-friendly.\n"
        )

        return system + "\n\n" + user

    def generate_plan(self, profile: Dict[str, Any], temperature: float = 0.3) -> Dict[str, Any]:
        prompt = self.build_prompt(profile)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=800
        )

        text = response.choices[0].message.content

        return {"markdown": text}
