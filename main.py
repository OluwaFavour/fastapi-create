import typer
from manage_setup import configure_manage_in_project
from utils import validate_project_name
from database_setup import (
    configure_database,
    configure_database_connection,
    configure_database_in_project,
)
from alembic_setup import alembic_folder_name_prompt, alembic_setup
from project_setup import spin_up_project
from dependency_setup import install_dependencies
from config_setup import configure_core_config_in_project
from main_setup import configure_main_in_project

app = typer.Typer(no_args_is_help=True)


@app.command()
def create(project_name: str = typer.Argument("", callback=validate_project_name)):
    """Create a new FastAPI project."""
    project_name = validate_project_name(project_name)
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


if __name__ == "__main__":
    app()
