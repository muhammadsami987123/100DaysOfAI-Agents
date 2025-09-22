from rich.progress import Progress, SpinnerColumn, TextColumn

class ComicRefactorer:
    def __init__(self, backend_type, ai_client, model_name, temperature, max_tokens):
        self.backend_type = backend_type
        self.ai_client = ai_client
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def refactor_draft(self, draft):
        generated_text = ""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            task = progress.add_task("[cyan]Analyzing and refactoring your draft...[/cyan]", total=100)
            
            if self.backend_type == "huggingface":
                progress.advance(task, 40)
                refactor_prompt = f"Refactor the following comic draft to improve its pacing, humor, and visual structure. Provide the improved script. Original draft: {draft}"
                generated_text = self.ai_client(refactor_prompt, max_length=700, num_return_sequences=1)[0]['generated_text']
                progress.advance(task, 60)
            elif self.backend_type == "openai":
                progress.advance(task, 40)
                response = self.ai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a comic script refactoring expert. Improve pacing, humor, and visual structure."},
                        {"role": "user", "content": f"Refactor the following comic draft: {draft}"}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                generated_text = response.choices[0].message.content.strip()
                progress.advance(task, 60)
            progress.remove_task(task)

        refactored_comic = f"# Refactored Comic Script\n\n{generated_text.strip()}\n\n"
        return refactored_comic
