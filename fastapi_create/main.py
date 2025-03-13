from pathlib import Path
import shutil
import typer
from fastapi_create.manage_setup import configure_manage_in_project
from fastapi_create.readme_setup import configure_readme_in_project
from fastapi_create.requirements_setup import generate_requirements_txt
from fastapi_create.utils import generate_base_path, validate_project_name
from fastapi_create.database_setup import (
    configure_database,
    configure_database_connection,
    configure_database_in_project,
)
from fastapi_create.alembic_setup import alembic_folder_name_prompt, alembic_setup
from fastapi_create.project_setup import spin_up_project
from fastapi_create.dependency_setup import install_dependencies
from fastapi_create.config_setup import configure_core_config_in_project
from fastapi_create.main_setup import configure_main_in_project

app = typer.Typer(no_args_is_help=True)


@app.command()
def create(project_name: str = typer.Argument("", callback=validate_project_name)):
    """Create a new FastAPI project."""
    project_name = validate_project_name(project_name)
    base_path: Path = generate_base_path(project_name)

    # Prevent overwriting existing directory unless it's empty
    if base_path.exists() and project_name != ".":
        if base_path.is_dir() and any(base_path.iterdir()):
            print(
                f"[red]Error: Directory '{base_path}' already exists and is not empty. Aborting.[/red]"
            )
            raise typer.Exit(1)
        elif base_path.is_file():
            print(
                f"[red]Error: '{base_path}' is a file, not a directory. Aborting.[/red]"
            )
            raise typer.Exit(1)

    try:
        db_dependency, db_url, db_thread_type = configure_database()
        alembic_folder_name = alembic_folder_name_prompt()
        base_path = spin_up_project(project_name)
        install_dependencies(db_thread_type)
        configure_database_connection(db_dependency, db_url, base_path)
        configure_database_in_project(db_thread_type, base_path)
        alembic_setup(alembic_folder_name, base_path)
        configure_core_config_in_project(base_path)
        configure_main_in_project(db_thread_type, base_path)
        configure_manage_in_project(base_path)
        configure_readme_in_project(base_path)
        generate_requirements_txt(base_path)
    except (Exception, SystemExit):
        if base_path and base_path.exists():
            print("[red]Cleaning up...[/red]")
            shutil.rmtree(base_path, ignore_errors=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
