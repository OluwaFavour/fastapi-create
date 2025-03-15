from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_main_code(db_thread_type: str) -> str:
    """
    Generate the main application code from a template.

    Args:
        db_thread_type (str): The type of database threading to use.
                              Should be "async" for asynchronous threading.

    Returns:
        str: The generated main application code as a string.
    """
    print("[yellow]Generating main code...[/yellow]")
    return generate_file_content(
        "main_template.py.jinja2", is_async=db_thread_type == "async"
    )


def configure_main_in_project(db_thread_type: str, base_path: Path) -> None:
    """
    Configure main application files in the project.

    Args:
        db_thread_type (str): The type of database threading to use.
        base_path (Path): The base path where the project is located.

    Returns:
        None
    """
    app_path = base_path / "app"
    print(f"[yellow]Writing main.py to the project...[/yellow]")
    content = generate_main_code(db_thread_type)
    write_file(app_path / "main.py", content)
    print("[green]main.py written successfully[/green]")
