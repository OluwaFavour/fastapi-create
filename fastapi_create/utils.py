from pathlib import Path
import secrets
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
