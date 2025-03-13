from pathlib import Path
from rich import print
from utils import load_template, write_file


def generate_lifespans_code(db_thread_type: str) -> str:
    """Generate lifespans code from a template."""
    print("[yellow]Generating lifespans code...[/yellow]")
    template_name = (
        f"{'sync' if db_thread_type == 'sync' else 'async'}_lifespans_template.py"
    )
    return load_template(template_name)


def generate_main_code() -> str:
    """Generate main application code from a template."""
    print("[yellow]Generating main code...[/yellow]")
    return load_template("main_template.py")


def configure_main_in_project(db_thread_type: str, base_path: Path) -> None:
    """Configure main application files in the project."""
    app_path = base_path / "app"
    for name, generator in [
        ("lifespans.py", generate_lifespans_code),
        ("main.py", generate_main_code),
    ]:
        print(f"[yellow]Writing {name} to the project...[/yellow]")
        content = generator(db_thread_type) if "lifespans" in name else generator()
        write_file(app_path / name, content)
        print(f"[green]{name} written successfully[/green]")
