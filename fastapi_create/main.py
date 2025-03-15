from pathlib import Path
import shutil
from time import sleep
from typing import Any
import typer
from rich import print
from rich.prompt import Prompt
from fastapi_create.core_dependencies_setup import (
    configure_core_dependencies_in_project,
)
from fastapi_create.manage_setup import configure_manage_in_project
from fastapi_create.readme_setup import configure_readme_in_project
from fastapi_create.requirements_setup import generate_requirements_txt
from fastapi_create.smtp_setup import (
    configure_core_messages_in_project,
    configure_smtp_settings,
)
from fastapi_create.utils import (
    clean_up,
    project_name_callback,
    generate_base_path,
)
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
def create(project_name: str = typer.Argument("", callback=project_name_callback)):
    """Create a new FastAPI project."""
    base_path: Path = generate_base_path(project_name)

    # Prevent overwriting existing directory unless it's empty
    if base_path.exists():
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
        # PROMPT USER FOR CONFIGURATION
        ## Prompt user for thread type
        thread_type = Prompt.ask(
            "Do you want your FastAPI application to be synchronous or asynchronous?",
            choices=["async", "sync"],
            default="async",
        )
        is_async = thread_type == "async"

        ## Prompt user for database configuration
        db_dependency, db_url = configure_database(is_async)

        ## Prompt user for SMTP configuration
        smtp_enabled = configure_smtp_settings(base_path)

        ## Prompt user for alembic configuration
        alembic_folder_name = alembic_folder_name_prompt()

        # Create project skeleton
        spin_up_project(project_name)

        # Install dependencies
        install_dependencies(base_path, is_async, db_dependency)
        configure_database_connection(db_url, base_path)
        configure_database_in_project(is_async, base_path)
        if smtp_enabled:
            configure_core_messages_in_project(base_path, is_async)
        configure_core_config_in_project(base_path, smtp_enabled)
        configure_core_dependencies_in_project(base_path, is_async)
        alembic_setup(alembic_folder_name, base_path, is_async)
        configure_main_in_project(is_async, base_path)
        configure_manage_in_project(base_path)
        configure_readme_in_project(base_path)
    except KeyboardInterrupt:
        print("[yellow]Input interrupted by user.[/yellow]")
        clean_up(base_path)
        typer.Exit()
    except (Exception, SystemExit):
        clean_up(base_path)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
