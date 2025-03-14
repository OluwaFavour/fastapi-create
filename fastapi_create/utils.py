from pathlib import Path
import secrets
from typing import Any, Callable, Tuple
from jinja2 import Environment, FileSystemLoader
import typer
from rich import print
from rich.prompt import Prompt
from dotenv import load_dotenv, set_key
from fastapi_create.constants import PROJECT_NAME_REGEX


def validate_project_name(project_name: str) -> str:
    """Validate the project name and prompt if empty."""
    if project_name == "":
        project_name = Prompt.ask("Enter the project name")
        return validate_project_name(project_name)
    if not PROJECT_NAME_REGEX.match(project_name) and project_name != ".":
        raise typer.BadParameter(
            "Invalid project name. Must be '.' or a valid Python identifier."
        )
    return project_name


def create_file(file_path: Path, content: str) -> None:
    """Create a file with the given content, ensuring parent directories exist."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    except (IOError, OSError) as e:
        print(f"[red]Error creating file {file_path}: {e}[/red]", file="stderr")
        raise RuntimeError(f"Error creating file {file_path}")


def write_file(file_path: Path, content: str) -> None:
    """Write content to a file."""
    try:
        file_path.write_text(content)
    except (IOError, OSError) as e:
        print(f"[red]Error writing to file {file_path}: {e}[/red]", file="stderr")
        raise RuntimeError(f"Error writing to file {file_path}")


def generate_secret_key() -> str:
    """Generate a random secret key."""
    return secrets.token_hex(32)


def add_key_value_to_env_file(env_path: Path, key: str, value: str) -> None:
    """Add a key-value pair to a .env file."""
    load_dotenv(env_path)
    set_key(str(env_path), key, value)


def generate_file_content(template_name: str, **kwargs) -> str:
    """Generate file content from a Jinja2 template."""
    print(f"[yellow]Generating {template_name.split('_template')[0]} code...[/yellow]")
    env = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))
    template = env.get_template(template_name)
    return template.render(**kwargs)


def generate_base_path(path_prefix: str | None = None) -> Path:
    base_path = Path.cwd() if path_prefix == "." else Path(path_prefix or "")
    if not base_path.is_absolute():
        base_path = Path.cwd() / base_path
    return base_path


def recursive_prompt_with_validation(
    prompt: str,
    error_msg: str,
    validation_func: Callable[..., bool],
    validation_args: Tuple[Any, ...] = (),
    validation_kwargs: dict[str, Any] | None = None,
    prompt_kwargs: dict[str, Any] | None = None,
) -> str:
    """Recursively prompt the user for input until it passes validation.

    Args:
        prompt: The message to display to the user.
        error_msg: The message to show if validation fails.
        validation_func: A function that takes the input and optional args, returning a boolean.
        validation_args: Additional positional arguments to pass to validation_func.
        validation_kwargs: Additional keyword arguments to pass to validation_func.
        prompt_kwargs: Additional arguments to pass to Prompt.ask and it can include any of the following:
        console: Console object to use for prompting.
        password: bool to hide user input.
        choices: List of valid choices.
        case_sensitive: bool to make choices case-sensitive.
        show_default: bool to show the default value.
        show_choices: bool to show the choices.
        default: Default value for the prompt.
        stream: Stream object to use for prompting.

    Returns:
        A string that passes the validation function.

    Raises:
        KeyboardInterrupt: If the user interrupts the prompt with Ctrl+C.
    """
    try:
        user_input = Prompt.ask(prompt=prompt, **prompt_kwargs)
        if not validation_func(user_input, *validation_args, **validation_kwargs):
            print(f"[red]{error_msg}[/red]")
            return recursive_prompt_with_validation(
                prompt,
                error_msg,
                validation_func,
                validation_args,
                validation_kwargs,
                prompt_kwargs,
            )
        return user_input
    except KeyboardInterrupt:
        print("[yellow]Input interrupted by user.[/yellow]")
        raise
