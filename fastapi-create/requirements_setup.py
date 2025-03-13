from pathlib import Path
import subprocess
import typer
from rich import print


def generate_requirements_txt(base_path: Path) -> None:
    """Generate requirements.txt content."""
    print("[yellow]Generating requirements.txt content...[/yellow]")
    try:
        with open(base_path / "requirements.txt", "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f, check=True)
        print("[green]requirements.txt content generated successfully[/green]")
    except subprocess.CalledProcessError:
        print("[red]Error generating requirements.txt[/red]", file="stderr")
        raise typer.Exit(code=1)
