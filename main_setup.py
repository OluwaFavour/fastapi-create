from pathlib import Path
from rich import print
from utils import generate_file_content, write_file


def generate_main_code(db_thread_type: str) -> str:
    """Generate main application code from a template."""
    print("[yellow]Generating main code...[/yellow]")
    return generate_file_content("main_template.py", is_async=db_thread_type == "async")


def configure_main_in_project(db_thread_type: str, base_path: Path) -> None:
    """Configure main application files in the project."""
    app_path = base_path / "app"
    print(f"[yellow]Writing main.py to the project...[/yellow]")
    content = generate_main_code(db_thread_type)
    write_file(app_path / "main.py", content)
    print("[green]main.py written successfully[/green]")
