from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file


def generate_core_config_code() -> str:
    """Generate core config code from a template."""
    print("[yellow]Generating core config code...[/yellow]")
    return generate_file_content("core_config_template.py.jinja2")


def configure_core_config_in_project(base_path: Path) -> None:
    """Write core config to the project."""
    config_path = base_path / "app" / "core" / "config.py"
    print("[yellow]Writing core config to the project...[/yellow]")
    write_file(config_path, generate_core_config_code())
    print("[green]Core config written successfully[/green]")
