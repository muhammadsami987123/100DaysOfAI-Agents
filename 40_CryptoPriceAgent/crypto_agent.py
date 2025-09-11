import json
import time
from typing import Dict, List, Optional, Tuple, Any
import requests
from datetime import datetime, timedelta

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore

try:
    from . import config
except ImportError:
    import config


class CoinGeckoAgent:
    """Agent for fetching cryptocurrency data from CoinGecko API"""
    
    def __init__(self):
        self.base_url = config.COINGECKO_API_BASE
        self.timeout = config.get_request_timeout()
        self.api_key = config.COINGECKO_API_KEY
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to CoinGecko API with error handling"""
        if params is None:
            params = {}
            
        # Add API key if available
        if self.api_key:
            params['x_cg_demo_api_key'] = self.api_key
            
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            return None
    
    def get_top_cryptos(self, limit: int = 10, currency: str = "usd") -> List[Dict]:
        """Get top cryptocurrencies by market cap"""
        params = {
            'vs_currency': currency,
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h'
        }
        
        data = self._make_request("coins/markets", params)
        if not data:
            return []
            
        return data
    
    def get_crypto_prices(self, crypto_ids: List[str], currency: str = "usd") -> Dict[str, Dict]:
        """Get current prices for specific cryptocurrencies"""
        if not crypto_ids:
            return {}
            
        ids_str = ",".join(crypto_ids)
        params = {
            'ids': ids_str,
            'vs_currencies': currency,
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true',
            'include_market_cap': 'true'
        }
        
        data = self._make_request("simple/price", params)
        if not data:
            return {}
            
        return data
    
    def get_crypto_info(self, crypto_id: str) -> Optional[Dict]:
        """Get detailed information about a specific cryptocurrency"""
        data = self._make_request(f"coins/{crypto_id}")
        return data
    
    def search_crypto(self, query: str) -> List[Dict]:
        """Search for cryptocurrencies by name or symbol"""
        params = {'query': query}
        data = self._make_request("search", params)
        if not data or 'coins' not in data:
            return []
        return data['coins']


class OpenAIAgent:
    """Agent for generating market insights using OpenAI GPT"""
    
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL
        self.client = None
        
        if self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key)
    
    def generate_market_insights(self, crypto_data: List[Dict], currency: str = "usd") -> Optional[str]:
        """Generate market insights based on current crypto data"""
        if not self.client or not crypto_data:
            return None
            
        # Prepare data for analysis
        market_summary = []
        for crypto in crypto_data[:5]:  # Top 5 for analysis
            change_24h = crypto.get('price_change_percentage_24h', 0)
            market_summary.append({
                'name': crypto.get('name', 'Unknown'),
                'symbol': crypto.get('symbol', '').upper(),
                'price': crypto.get('current_price', 0),
                'change_24h': change_24h,
                'market_cap': crypto.get('market_cap', 0)
            })
        
        prompt = f"""
        Analyze the following cryptocurrency market data and provide a brief market insight (2-3 sentences):
        
        Market Data (in {currency.upper()}):
        {json.dumps(market_summary, indent=2)}
        
        Focus on:
        1. Overall market sentiment based on 24h changes
        2. Notable trends or patterns
        3. Brief risk assessment
        
        Keep the response concise and professional.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cryptocurrency market analyst. Provide concise, professional insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def analyze_portfolio_risk(self, portfolio_data: Dict) -> Optional[str]:
        """Analyze portfolio risk based on holdings and market data"""
        if not self.client or not portfolio_data:
            return None
            
        prompt = f"""
        Analyze this cryptocurrency portfolio for risk assessment:
        
        Portfolio Data:
        {json.dumps(portfolio_data, indent=2)}
        
        Provide a brief risk analysis (2-3 sentences) covering:
        1. Overall portfolio risk level (Low/Medium/High)
        2. Key risk factors
        3. Brief recommendation
        
        Keep it concise and professional.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cryptocurrency portfolio risk analyst. Provide concise, professional risk assessments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None


class PortfolioManager:
    """Manages user's cryptocurrency portfolio"""
    
    def __init__(self):
        self.portfolio_path = config.get_portfolio_path()
        self.portfolio = self._load_portfolio()
    
    def _load_portfolio(self) -> Dict:
        """Load portfolio from file"""
        try:
            with open(self.portfolio_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"holdings": {}, "currency": "usd", "last_updated": None}
    
    def _save_portfolio(self) -> bool:
        """Save portfolio to file"""
        try:
            self.portfolio["last_updated"] = datetime.now().isoformat()
            with open(self.portfolio_path, 'w') as f:
                json.dump(self.portfolio, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save portfolio: {e}")
            return False
    
    def add_holding(self, crypto_id: str, amount: float, purchase_price: float = None) -> bool:
        """Add or update a cryptocurrency holding"""
        if crypto_id not in self.portfolio["holdings"]:
            self.portfolio["holdings"][crypto_id] = {
                "amount": 0,
                "purchase_price": 0,
                "total_invested": 0
            }
        
        holding = self.portfolio["holdings"][crypto_id]
        holding["amount"] += amount
        
        if purchase_price:
            holding["purchase_price"] = purchase_price
            holding["total_invested"] += amount * purchase_price
        
        return self._save_portfolio()
    
    def remove_holding(self, crypto_id: str, amount: float = None) -> bool:
        """Remove or reduce a cryptocurrency holding"""
        if crypto_id not in self.portfolio["holdings"]:
            return False
        
        holding = self.portfolio["holdings"][crypto_id]
        
        if amount is None or amount >= holding["amount"]:
            # Remove completely
            del self.portfolio["holdings"][crypto_id]
        else:
            # Reduce amount
            holding["amount"] -= amount
            holding["total_invested"] = holding["total_invested"] * (holding["amount"] / (holding["amount"] + amount))
        
        return self._save_portfolio()
    
    def get_portfolio(self) -> Dict:
        """Get current portfolio"""
        return self.portfolio
    
    def get_portfolio_value(self, crypto_agent: CoinGeckoAgent, currency: str = "usd") -> Dict:
        """Calculate current portfolio value"""
        holdings = self.portfolio["holdings"]
        if not holdings:
            return {"total_value": 0, "total_invested": 0, "pnl": 0, "pnl_percentage": 0, "holdings": {}}
        
        crypto_ids = list(holdings.keys())
        prices = crypto_agent.get_crypto_prices(crypto_ids, currency)
        
        total_value = 0
        total_invested = 0
        holdings_data = {}
        
        for crypto_id, holding in holdings.items():
            if crypto_id in prices:
                current_price = prices[crypto_id].get(currency, 0)
                amount = holding["amount"]
                invested = holding["total_invested"]
                
                current_value = amount * current_price
                pnl = current_value - invested
                pnl_percentage = (pnl / invested * 100) if invested > 0 else 0
                
                holdings_data[crypto_id] = {
                    "amount": amount,
                    "current_price": current_price,
                    "current_value": current_value,
                    "invested": invested,
                    "pnl": pnl,
                    "pnl_percentage": pnl_percentage
                }
                
                total_value += current_value
                total_invested += invested
        
        overall_pnl = total_value - total_invested
        overall_pnl_percentage = (overall_pnl / total_invested * 100) if total_invested > 0 else 0
        
        return {
            "total_value": total_value,
            "total_invested": total_invested,
            "pnl": overall_pnl,
            "pnl_percentage": overall_pnl_percentage,
            "holdings": holdings_data
        }
    
    def set_currency(self, currency: str) -> bool:
        """Set portfolio display currency"""
        self.portfolio["currency"] = currency.lower()
        return self._save_portfolio()


class RiskAnalyzer:
    """Analyzes cryptocurrency risk based on market data"""
    
    @staticmethod
    def calculate_risk_level(change_24h: float) -> Tuple[str, str]:
        """Calculate risk level based on 24h price change"""
        abs_change = abs(change_24h)
        
        if abs_change < 5:
            return "Low", "🟢"
        elif abs_change < 15:
            return "Medium", "🟡"
        else:
            return "High", "🔴"
    
    @staticmethod
    def analyze_portfolio_risk(portfolio_value: Dict) -> Dict:
        """Analyze overall portfolio risk"""
        holdings = portfolio_value.get("holdings", {})
        if not holdings:
            return {"risk_level": "Unknown", "risk_emoji": "⚪", "factors": []}
        
        risk_factors = []
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        for crypto_id, holding in holdings.items():
            # This would need 24h change data from the crypto agent
            # For now, we'll use PnL percentage as a proxy
            pnl_pct = holding.get("pnl_percentage", 0)
            abs_pnl = abs(pnl_pct)
            
            if abs_pnl > 20:
                high_risk_count += 1
                risk_factors.append(f"{crypto_id}: High volatility ({pnl_pct:.1f}%)")
            elif abs_pnl > 10:
                medium_risk_count += 1
            else:
                low_risk_count += 1
        
        # Determine overall risk
        total_holdings = len(holdings)
        if high_risk_count > total_holdings * 0.5:
            risk_level, risk_emoji = "High", "🔴"
        elif medium_risk_count > total_holdings * 0.3:
            risk_level, risk_emoji = "Medium", "🟡"
        else:
            risk_level, risk_emoji = "Low", "🟢"
        
        return {
            "risk_level": risk_level,
            "risk_emoji": risk_emoji,
            "factors": risk_factors[:3],  # Top 3 risk factors
            "high_risk_count": high_risk_count,
            "medium_risk_count": medium_risk_count,
            "low_risk_count": low_risk_count
        }
