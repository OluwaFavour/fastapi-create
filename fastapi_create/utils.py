from pathlib import Path
import secrets
import shutil
import subprocess
from typing import Any, Callable, Tuple
from jinja2 import Environment, FileSystemLoader
import typer
from rich import print
from rich.prompt import Prompt
from dotenv import load_dotenv, set_key
from fastapi_create.constants import PROJECT_NAME_REGEX


def validate_project_name(project_name: str) -> bool:
    """
    Validate the project name to ensure it is either a '.' or a valid directory name.

    Args:
        project_name (str): The name of the project to validate.

    Returns:
        bool: True if the project name is valid, False otherwise.
    """
    if not PROJECT_NAME_REGEX.match(project_name) and project_name != ".":
        print(
            "[red]Error: Invalid project name. Must be '.' or a valid directory name.[/red]"
        )
        return False
    return True


def project_name_callback(project_name: str) -> str:
    """
    Callback function to validate and process the project name.
    If the provided project name is an empty string, it prompts the user to enter a valid project name.
    If the provided project name is not valid, it raises a BadParameter exception.
    Args:
        project_name (str): The name of the project to validate.
    Returns:
        str: The validated project name.
    Raises:
        typer.BadParameter: If the project name is not valid.
    """
    if project_name.strip() == "":
        project_name = recursive_prompt_with_validation(
            prompt="Enter the project name", validation_func=validate_project_name
        )
    else:
        if not validate_project_name(project_name):
            raise typer.BadParameter(
                "[red]Error: Invalid project name. Must be '.' or a valid Python identifier.[/red]"
            )

    return project_name


def create_file(file_path: Path, content: str) -> None:
    """
    Create a file with the given content, ensuring parent directories exist.

    Args:
        file_path (Path): The path where the file will be created.
        content (str): The content to write to the file.

    Raises:
        RuntimeError: If there is an error creating the file.
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    except (IOError, OSError) as e:
        print(f"[red]Error creating file {file_path}: {e}[/red]", file="stderr")
        raise RuntimeError(f"Error creating file {file_path}")


def write_file(file_path: Path, content: str) -> None:
    """
    Write content to a file.

    Args:
        file_path (Path): The path to the file where the content will be written.
        content (str): The content to write to the file.

    Raises:
        RuntimeError: If there is an error writing to the file.
    """
    try:
        file_path.write_text(content)
    except (IOError, OSError) as e:
        print(f"[red]Error writing to file {file_path}: {e}[/red]", file="stderr")
        raise RuntimeError(f"Error writing to file {file_path}")


def generate_secret_key() -> str:
    """
    Generate a random secret key.

    Returns:
        str: A randomly generated secret key in hexadecimal format.
    """
    return secrets.token_hex(32)


def add_key_value_to_env_file(env_path: Path, key: str, value: str) -> None:
    """
    Add a key-value pair to a .env file.

    This function loads the environment variables from the specified .env file,
    adds or updates the given key-value pair, and saves the changes back to the file.

    Args:
        env_path (Path): The path to the .env file.
        key (str): The key to add or update in the .env file.
        value (str): The value to associate with the key.

    Returns:
        None
    """
    load_dotenv(env_path)
    set_key(str(env_path), key, value)


def generate_file_content(template_name: str, **kwargs) -> str:
    """
    Generate file content from a Jinja2 template.

    This function loads a Jinja2 template from the "templates" directory located
    in the same directory as this script, and renders it with the provided keyword
    arguments.

    Args:
        template_name (str): The name of the Jinja2 template file.
        **kwargs: Arbitrary keyword arguments to be passed to the template for rendering.

    Returns:
        str: The rendered content of the template as a string.
    """
    print(f"[yellow]Generating {template_name.split('_template')[0]} code...[/yellow]")
    env = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))
    template = env.get_template(template_name)
    return template.render(**kwargs)


def generate_base_path(path_prefix: str | None = None) -> Path:
    """
    Generates an absolute base path based on the provided path prefix.

    Args:
        path_prefix (str | None): The prefix to use for generating the base path.
                                  If None or an empty string is provided, the current working directory is used.
                                  If "." is provided, the current working directory is used.

    Returns:
        Path: An absolute Path object representing the base path.
    """
    base_path = Path.cwd() if path_prefix == "." else Path(path_prefix or "")
    if not base_path.is_absolute():
        base_path = Path.cwd() / base_path
    return base_path


def recursive_prompt_with_validation(
    prompt: str,
    validation_func: Callable[..., bool],
    validation_args: Tuple[Any, ...] = (),
    validation_kwargs: dict[str, Any] | None = {},
    error_msg: str | None = None,
    prompt_kwargs: dict[str, Any] = {},
) -> str:
    """Recursively prompt the user for input until it passes validation.

    Args:
        prompt: The message to display to the user.
        validation_func: A function that takes the input and optional args, returning a boolean.
        validation_args: Additional positional arguments to pass to validation_func.
        validation_kwargs: Additional keyword arguments to pass to validation_func.
        error_msg: Optional message to show if validation fails.
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
    user_input = Prompt.ask(prompt=prompt, **prompt_kwargs)
    if not validation_func(user_input, *validation_args, **validation_kwargs):
        if error_msg:
            print(f"[red]{error_msg}[/red]")
        return recursive_prompt_with_validation(
            prompt,
            validation_func,
            validation_args,
            validation_kwargs,
            error_msg,
            prompt_kwargs,
        )
    return user_input


def uninstall_dependencies(base_path: Path) -> None:
    """
    Uninstall dependencies listed in the requirements.txt file located at the given base path.

    This function performs the following steps:
    1. Prints a message indicating that dependencies are being uninstalled.
    2. Attempts to uninstall the dependencies listed in the requirements.txt file using pip.
    3. Deletes the requirements.txt file after successful uninstallation.
    4. Prints a success message if the uninstallation is successful.
    5. Raises a RuntimeError if there is an error during the uninstallation process.

    Args:
        base_path (Path): The base path where the requirements.txt file is located.

    Raises:
        RuntimeError: If there is an error uninstalling the dependencies.
    """
    print("[yellow]Uninstalling dependencies...[/yellow]")
    try:
        requirements_path = base_path / "requirements.txt"
        subprocess.run(
            ["pip", "uninstall", "-r", str(requirements_path), "-y"], check=True
        )
        print("[yellow]Deleting requirements.txt...[/yellow]")
        requirements_path.unlink()
    except subprocess.CalledProcessError:
        print("[red]Error uninstalling dependencies[/red]", file="stderr")
        raise RuntimeError("Error uninstalling dependencies")
    print("[green]Dependencies uninstalled successfully[/green]")


def clean_up(base_path: Path) -> None:
    """
    Remove the project directory if an error occurs.

    This function performs the following steps:
    1. Checks if the provided base_path exists.
    2. Prints a message indicating the start of the cleanup process.
    3. Uninstalls any dependencies associated with the project.
    4. Removes the project directory and its contents.
    5. Prints a message indicating the completion of the cleanup process.

    Args:
        base_path (Path): The path to the project directory to be removed.

    Returns:
        None
    """
    if base_path and base_path.exists():
        print("[red]Cleaning up...[/red]")
        # Uninstall dependencies
        uninstall_dependencies(base_path)
        print(f"[yellow]Removing {base_path}...[/yellow]")
        shutil.rmtree(base_path, ignore_errors=True)
        print("[green]Clean up complete[/green]")


def get_plural_name(name: str) -> str:
    """
    Get the plural form of a word.

    Args:
        name (str): The singular form of the word.

    Returns:
        str: The plural form of the word.
    """
    if name.endswith("y"):
        return name[:-1] + "ies"
    elif (
        name.endswith("s")
        or name.endswith("x")
        or name.endswith("z")
        or name.endswith("ch")
        or name.endswith("sh")
    ):
        return name + "es"
    else:
        return name + "s"
