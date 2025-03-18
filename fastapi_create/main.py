from pathlib import Path
from typing import Any
import typer
from rich import print
from rich.prompt import Prompt, Confirm
from fastapi_create.auth_setup import handle_auth_setup
from fastapi_create.core_dependencies_setup import (
    configure_core_dependencies_in_project,
)
from fastapi_create.manage_setup import configure_manage_in_project
from fastapi_create.readme_setup import configure_readme_in_project
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
from fastapi_create.auth_router_setup import configure_auth_router_in_project
from fastapi_create.auth_schema_setup import configure_auth_schema_in_project
from fastapi_create.core_utils_security_setup import (
    configure_core_utils_security_in_project,
)
from fastapi_create.core_utils_validators_setup import (
    configure_core_utils_validators_in_project,
)
from fastapi_create.auth_db_models_setup import configure_db_models_in_project

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

        ## Prompt user for Auth configuration
        auth_enabled = Confirm.ask(
            "Do you want to include authentication and authorization?", default=True
        )
        if auth_enabled:
            auth_system = Prompt.ask(
                "Which authentication system do you want to use?",
                choices=["JWT", "Session"],
                default="JWT",
                case_sensitive=False,
            ).lower()
            auth_model, required_fields, login_field = handle_auth_setup()
            username_is_required = "username" in required_fields
            email_is_required = "email" in required_fields
            phone_is_required = "phone" in required_fields
            verification_enabled = (
                Confirm.ask(
                    "Do you want to include email verification for user registration?",
                    default=True,
                )
                if smtp_enabled
                else False
            )
        else:
            (
                auth_system,
                auth_model,
                required_fields,
                login_field,
                verification_enabled,
                username_is_required,
                email_is_required,
                phone_is_required,
            ) = (
                None,
                None,
                None,
                None,
                False,
                False,
                False,
                False,
            )

        ## Prompt user for alembic configuration
        alembic_include = Confirm.ask(
            "Do you want to include Alembic migrations?",
            default=True,
        )

        ## Prompt user for alembic folder name
        alembic_folder_name = alembic_folder_name_prompt() if alembic_include else None

        ## Prompt user for CORS configuration
        cors_enabled = Confirm.ask(
            "Do you want to include CORS middleware?",
            default=True,
        )

        # Create project skeleton
        spin_up_project(project_name)

        # Install dependencies
        install_dependencies(base_path, is_async, db_dependency, auth_system)

        # Configure database connection
        configure_database_connection(db_url, base_path)

        # Configure database in project
        configure_database_in_project(is_async, base_path)
        if smtp_enabled:
            configure_core_messages_in_project(
                base_path, is_async
            )  # Configure core messages
        configure_core_config_in_project(
            base_path, auth_system, cors_enabled, smtp_enabled, verification_enabled
        )  # Configure core config
        configure_core_dependencies_in_project(
            base_path,
            is_async,
            auth_model,
            auth_system,
            auth_enabled,
            smtp_enabled,
            verification_enabled,
        )  # Configure core dependencies
        if alembic_include:
            # Configure Alembic if enabled
            alembic_setup(alembic_folder_name, base_path, is_async)
        configure_main_in_project(
            is_async, base_path, cors_enabled, auth_enabled
        )  # Configure main
        configure_manage_in_project(base_path)  # Configure manage.py
        configure_readme_in_project(base_path)  # Configure README
        if auth_enabled:
            # Configure authentication if enabled
            # configure_auth_in_project(base_path, is_async, auth_system, verification_enabled)
            configure_core_utils_security_in_project(
                base_path, verification_enabled, auth_system
            )  # Configure core utils security
            configure_core_utils_validators_in_project(
                base_path,
            )  # Configure core utils validators
            configure_db_models_in_project(
                base_path,
                auth_model,
                login_field,
                is_async,
                email_is_required,
                phone_is_required,
                username_is_required,
                verification_enabled,
            )  # Configure db models
            configure_auth_router_in_project(
                base_path,
                auth_model,
                auth_system,
                login_field,
                email_is_required,
                phone_is_required,
                username_is_required,
                is_async,
                verification_enabled,
            )  # Configure auth router
            configure_auth_schema_in_project(
                base_path,
                auth_model,
                auth_system,
                login_field,
                email_is_required,
                phone_is_required,
                username_is_required,
                verification_enabled,
            )  # Configure auth schema
    except KeyboardInterrupt:
        print("[yellow]Input interrupted by user.[/yellow]")
        clean_up(base_path)
        typer.Exit()
    except (Exception, SystemExit) as e:
        print(f"[red]Error: {e}[/red]")
        clean_up(base_path)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
