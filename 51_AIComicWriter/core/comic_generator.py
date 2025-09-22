from rich.progress import Progress, SpinnerColumn, TextColumn

class ComicGenerator:
    def __init__(self, backend_type, ai_client, model_name, temperature, max_tokens):
        self.backend_type = backend_type
        self.ai_client = ai_client
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate_comic(self, topic, characters, tone, panels):
        prompt = f"Generate a {tone} comic script about {topic} with characters {characters} in {panels} panels. Each panel should have a visual description and dialogue.\n\nComic Script:"

        generated_text = ""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            task = progress.add_task("[cyan]Brainstorming and writing your comic...[/cyan]", total=100)
            
            if self.backend_type == "huggingface":
                progress.advance(task, 20)
                generated_text = self.ai_client(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']
                progress.advance(task, 80)
            elif self.backend_type == "openai":
                progress.advance(task, 20)
                response = self.ai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a creative comic script writer. Generate structured comic panels with visual descriptions and dialogue."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                generated_text = response.choices[0].message.content.strip()
                progress.advance(task, 80)
            progress.remove_task(task)
        
        comic_script = f"# Comic Script: {topic.title()}\n\n"
        comic_script += f"**Characters:** {characters if characters else 'N/A'}\n"
        comic_script += f"**Tone:** {tone.title()}\n"
        comic_script += f"**Panels:** {panels}\n\n"
        comic_script += "---\n\n"

        panels_content = generated_text.split("Panel")
        
        actual_panels_start = 0
        for i, p_text in enumerate(panels_content):
            if "visual" in p_text.lower() or "dialogue" in p_text.lower() or f"panel {i+1}" in p_text.lower():
                actual_panels_start = i
                break
        panels_content = panels_content[actual_panels_start:]

        for i, panel_text in enumerate(panels_content[:panels]):
            cleaned_panel_text = panel_text.replace(f"{i+1}:", "").strip()
            if not cleaned_panel_text.lower().startswith("panel "):
                 comic_script += f"## Panel {i+1}\n\n{cleaned_panel_text}\n\n"
            else:
                comic_script += f"## {cleaned_panel_text}\n\n"
        return comic_script
