from rich.progress import Progress, SpinnerColumn, TextColumn

class RandomIdeaGenerator:
    def __init__(self, backend_type, ai_client, model_name, temperature, max_tokens):
        self.backend_type = backend_type
        self.ai_client = ai_client
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def suggest_idea(self):
        generated_idea_text = ""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            task = progress.add_task("[cyan]Brewing a fresh idea...[/cyan]", total=100)
            
            if self.backend_type == "huggingface":
                progress.advance(task, 30)
                random_prompt = "Generate a funny and creative comic idea with a title and a logline."
                generated_idea_text = self.ai_client(random_prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
                progress.advance(task, 70)
            elif self.backend_type == "openai":
                progress.advance(task, 30)
                response = self.ai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a creative idea generator. Provide concise and engaging comic ideas."},
                        {"role": "user", "content": "Generate a fresh, creative comic idea with a short logline and title."}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                generated_idea_text = response.choices[0].message.content.strip()
                progress.advance(task, 70)
            progress.remove_task(task)

        title = "" 
        logline = ""
        lines = generated_idea_text.split('\n')
        for line in lines:
            if "Title:" in line: 
                title = line.replace("Title:", "").strip()
            elif "Logline:" in line:
                logline = line.replace("Logline:", "").strip()
        
        if not title and not logline:
            title = "A Quirky Adventure"
            logline = generated_idea_text.strip()

        random_idea_output = f"# Random Comic Idea\n\nTitle: {title}\nLogline: {logline}\n\n"
        return random_idea_output
