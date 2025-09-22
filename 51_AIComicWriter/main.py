import click
import os
import sys
from config import get_ai_backend
from utils.cli_interface import CLIInterface
from core.comic_generator import ComicGenerator
from core.random_idea_generator import RandomIdeaGenerator
from core.comic_refactorer import ComicRefactorer

cli_interface = CLIInterface()

@click.group()
@click.version_option("1.0.0", 
                      prog_name="AIComicWriter CLI",
                      message="%(prog)s version %(version)s")
@click.option('--use-openai', is_flag=True, help='Use OpenAI API for generation (requires OPENAI_API_KEY).')
@click.pass_context
def cli(ctx, use_openai):
    """AIComicWriter: Your creative comic script generator.
    
    Options:
      1. Generate Comic from Prompt
      2. Suggest a Random Comic Idea
      3. Refactor My Comic Draft
    """
    ctx.ensure_object(dict)
    ctx.obj['USE_OPENAI'] = use_openai
    pass

def save_comic_script(content, filename):
    if cli_interface.confirm_action(f"Do you want to save the comic script to {filename}?"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            cli_interface.print_success(f"Comic script saved to [green]{filename}[/green]")
        except IOError as e:
            cli_interface.print_error(f"Error saving file: {e}")
    else:
        cli_interface.print_info("Save cancelled.")

@cli.command()
@click.option('--topic', required=True, help='Topic for the comic.')
@click.option('--characters', help='Comma-separated character names.')
@click.option('--tone', default='funny', type=click.Choice(['funny', 'dramatic', 'dark', 'action', 'sci-fi', 'fantasy']), help='Tone of the comic.')
@click.option('--panels', type=int, default=6, help='Desired number of panels.')
@click.option('--format', default='markdown', type=click.Choice(['markdown', 'text']), help='Output format for the comic script.')
@click.option('--save', type=str, help='Filename to save the comic script (e.g., comic.md).')
@click.pass_context
def generate(ctx, topic, characters, tone, panels, format, save):
    """Generate a comic from a prompt."""
    backend_type, ai_client, model_name, temperature, max_tokens = get_ai_backend(ctx.obj['USE_OPENAI'])

    if backend_type == "none":
        cli_interface.print_error("No AI backend available. Please check your setup (OpenAI API key or Hugging Face model).")
        return

    generator = ComicGenerator(backend_type, ai_client, model_name, temperature, max_tokens)
    cli_interface.print_header(f"Generating {tone.title()} Comic about {topic.title()}")
    
    try:
        comic_script = generator.generate_comic(topic, characters, tone, panels)
    except Exception as e:
        cli_interface.print_error(f"Error during comic generation: {e}")
        return

    if format == 'text':
        comic_script = comic_script.replace('#', '').replace('**', '').replace('\n\n', '\n')

    if save:
        save_comic_script(comic_script, save)
    else:
        cli_interface.print_comic_script(comic_script, format=format)


@cli.command()
@click.option('--save', type=str, help='Filename to save the comic idea (e.g., idea.md).')
@click.option('--format', default='markdown', type=click.Choice(['markdown', 'text']), help='Output format for the comic idea.')
@click.pass_context
def random(ctx, save, format):
    """Suggest a random comic idea."""
    backend_type, ai_client, model_name, temperature, max_tokens = get_ai_backend(ctx.obj['USE_OPENAI'])

    if backend_type == "none":
        cli_interface.print_error("No AI backend available. Please check your setup (OpenAI API key or Hugging Face model).")
        return
    
    random_gen = RandomIdeaGenerator(backend_type, ai_client, model_name, temperature, max_tokens)
    cli_interface.print_header("Suggesting a Random Comic Idea")
    
    try:
        random_idea_output = random_gen.suggest_idea()
    except Exception as e:
        cli_interface.print_error(f"Error generating random idea: {e}")
        return

    if format == 'text':
        random_idea_output = random_idea_output.replace('#', '').replace('\n\n', '\n')

    if save:
        save_comic_script(random_idea_output, save)
    else:
        cli_interface.print_markdown(random_idea_output, title="Random Comic Idea")

@cli.command()
@click.option('--save', type=str, help='Filename to save the refactored comic (e.g., refactored_comic.md).')
@click.option('--format', default='markdown', type=click.Choice(['markdown', 'text']), help='Output format for the refactored comic.')
@click.pass_context
def refactor(ctx, save, format):
    """Refactor a pasted comic draft."""
    backend_type, ai_client, model_name, temperature, max_tokens = get_ai_backend(ctx.obj['USE_OPENAI'])

    if backend_type == "none":
        cli_interface.print_error("No AI backend available. Please check your setup (OpenAI API key or Hugging Face model).")
        return

    refactorer = ComicRefactorer(backend_type, ai_client, model_name, temperature, max_tokens)
    cli_interface.print_header("Refactoring Your Comic Draft")
    cli_interface.print_info("Paste your comic draft below. Press Ctrl+D (or Ctrl+Z on Windows) followed by Enter when you're done:")
    
    draft_lines = []
    while True:
        try:
            line = input()
            draft_lines.append(line)
        except EOFError:
            break
    
    draft = "\n".join(draft_lines)
    
    if not draft.strip():
        cli_interface.print_warning("No comic draft provided for refactoring.")
        return

    try:
        refactored_comic = refactorer.refactor_draft(draft)
    except Exception as e:
        cli_interface.print_error(f"Error during refactoring: {e}")
        return

    if format == 'text':
        refactored_comic = refactored_comic.replace('#', '').replace('**', '').replace('\n\n', '\n')

    if save:
        save_comic_script(refactored_comic, save)
    else:
        cli_interface.print_comic_script(refactored_comic, title="Refactored Comic Script", format=format)

if __name__ == '__main__':
    cli_interface.print_welcome()
    
    # Check if any direct command-line arguments are provided
    if len(sys.argv) == 1: # Only 'python main.py' is given
        # Interactive menu mode
        while True:
            choice = cli_interface.show_main_menu()

            if choice == "1": # Generate Comic
                topic = cli_interface.get_user_input("Enter topic for the comic", default="A brave knight on a quest")
                if not topic.strip():
                    cli_interface.print_warning("Topic cannot be empty. Please provide a topic.")
                    continue
                
                characters = cli_interface.get_user_input("Enter comma-separated character names", default="Sir Lancelot, Dragon")
                tone = cli_interface.get_user_input("Enter tone (funny, dramatic, dark, etc.)", default="funny")
                panels_str = cli_interface.get_user_input("Enter number of panels (default: 6)", default="6")
                panels = int(panels_str) if panels_str.isdigit() else 6
                save = cli_interface.get_user_input("Enter filename to save (optional, e.g., my_comic.md)", default="")
                format_output = cli_interface.get_user_input("Enter output format (markdown or text)", default="markdown")
                use_openai_flag = cli_interface.confirm_action("Use OpenAI API for this generation?")
                
                try:
                    backend_type, ai_client, model_name, temperature, max_tokens = get_ai_backend(use_openai_flag)
                    if backend_type == "none":
                        cli_interface.print_error("No AI backend available. Please check your setup (OpenAI API key or Hugging Face model).")
                        continue
                    generator = ComicGenerator(backend_type, ai_client, model_name, temperature, max_tokens)
                    comic_script = generator.generate_comic(topic, characters, tone, panels)
                    
                    if format_output == 'text':
                        comic_script = comic_script.replace('#', '').replace('**', '').replace('\n\n', '\n')
                    
                    if save:
                        save_comic_script(comic_script, save)
                    else:
                        cli_interface.print_comic_script(comic_script, format=format_output)
                    
                    if cli_interface.confirm_action("Copy generated comic script to clipboard?"):
                        cli_interface.copy_to_clipboard(comic_script)

                except Exception as e:
                    cli_interface.print_error(f"An error occurred during comic generation: {e}")
                
            elif choice == "2": # Suggest a Random Comic Idea
                save = cli_interface.get_user_input("Enter filename to save (optional, e.g., random_idea.md)", default="")
                format_output = cli_interface.get_user_input("Enter output format (markdown or text)", default="markdown")
                use_openai_flag = cli_interface.confirm_action("Use OpenAI API for this suggestion?")

                try:
                    backend_type, ai_client, model_name, temperature, max_tokens = get_ai_backend(use_openai_flag)
                    if backend_type == "none":
                        cli_interface.print_error("No AI backend available. Please check your setup (OpenAI API key or Hugging Face model).")
                        continue
                    random_gen = RandomIdeaGenerator(backend_type, ai_client, model_name, temperature, max_tokens)
                    random_idea_output = random_gen.suggest_idea()

                    if format_output == 'text':
                        random_idea_output = random_idea_output.replace('#', '').replace('\n\n', '\n')
                    
                    if save:
                        save_comic_script(random_idea_output, save)
                    else:
                        cli_interface.print_markdown(random_idea_output, title="Random Comic Idea")
                    
                    if cli_interface.confirm_action("Copy generated random idea to clipboard?"):
                        cli_interface.copy_to_clipboard(random_idea_output)

                except Exception as e:
                    cli_interface.print_error(f"An error occurred during random idea generation: {e}")

            elif choice == "3": # Refactor My Comic Draft
                save = cli_interface.get_user_input("Enter filename to save (optional, e.g., refactored_comic.md)", default="")
                format_output = cli_interface.get_user_input("Enter output format (markdown or text)", default="markdown")
                use_openai_flag = cli_interface.confirm_action("Use OpenAI API for this refactoring?")
                
                cli_interface.print_info("Paste your comic draft below. Press Ctrl+D (or Ctrl+Z on Windows) followed by Enter when you're done:")
                draft_lines = []
                while True:
                    try:
                        line = input()
                        draft_lines.append(line)
                    except EOFError:
                        break
                
                draft = "\n".join(draft_lines)
                
                if not draft.strip():
                    cli_interface.print_warning("No comic draft provided for refactoring.")
                    continue

                try:
                    backend_type, ai_client, model_name, temperature, max_tokens = get_ai_backend(use_openai_flag)
                    if backend_type == "none":
                        cli_interface.print_error("No AI backend available. Please check your setup (OpenAI API key or Hugging Face model).")
                        continue
                    refactorer = ComicRefactorer(backend_type, ai_client, model_name, temperature, max_tokens)
                    refactored_comic = refactorer.refactor_draft(draft)
                    
                    if format_output == 'text':
                        refactored_comic = refactored_comic.replace('#', '').replace('**', '').replace('\n\n', '\n')
                    
                    if save:
                        save_comic_script(refactored_comic, save)
                    else:
                        cli_interface.print_comic_script(refactored_comic, title="Refactored Comic Script", format=format_output)
                    
                    if cli_interface.confirm_action("Copy refactored comic script to clipboard?"):
                        cli_interface.copy_to_clipboard(refactored_comic)

                except Exception as e:
                    cli_interface.print_error(f"An error occurred during comic refactoring: {e}")

            elif choice in ["0", "exit", "quit", "q"]:
                cli_interface.print_info("Goodbye! 👋")
                break
            elif choice == "--help" or choice == "4": # Added option '4' for help
                cli_interface.print_help()
            else:
                cli_interface.print_warning("Invalid option. Please choose from 1, 2, 3, 4, or 0 to exit.")
    else:
        # If direct arguments are provided, let click handle them
        try:
            cli(obj={})
        except Exception as e:
            cli_interface.print_error(f"Error processing direct command: {e}")