from pathlib import Path
import subprocess
import typer
from rich import print


def generate_requirements_txt(base_path: Path) -> None:
    """
    Generate the content for a requirements.txt file by freezing the current
    Python environment's installed packages.

    Args:
        base_path (Path): The base directory where the requirements.txt file
                          will be created.

    Raises:
        RuntimeError: If there is an error during the generation of the
                      requirements.txt file.
    """
    print("[yellow]Generating requirements.txt content...[/yellow]")
    try:
        with open(base_path / "requirements.txt", "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f, check=True)
        print("[green]requirements.txt content generated successfully[/green]")
    except subprocess.CalledProcessError:
        print("[red]Error generating requirements.txt[/red]", file="stderr")
        raise RuntimeError("Error generating requirements.txt")
