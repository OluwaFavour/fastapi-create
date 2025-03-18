from pathlib import Path
from rich import print
from fastapi_create.utils import generate_file_content, write_file, get_plural_name


def generate_db_models_code(
    auth_model: str,
    login_field: str,
    is_async: bool,
    email_is_required: bool,
    phone_is_required: bool,
    username_is_required: bool,
    verification_enabled: bool,
) -> str:
    """
    Generate database models code from a template.

    This function prints a message indicating that the database models
    code is being generated, and then it generates the content of the database models
    file using a Jinja2 template.

    Args:
        auth_model (str): The name of the authentication model.
        login_field (str): The field used for login (e.g., "email" or "username").
        is_async (bool): Whether the application is using asynchronous dependencies.
        email_is_required (bool): Whether the email field is required.
        phone_is_required (bool): Whether the phone field is required.
        username_is_required (bool): Whether the username field is required.
        verification_enabled (bool): Whether email verification is enabled.

    Returns:
        str: The generated database models code as a string.
    """
    print("[yellow]Generating database models code...[/yellow]")
    return generate_file_content(
        "auth_models_template.py.jinja2",
        auth_model=auth_model,
        auth_model_plural=get_plural_name(auth_model),
        login_field=login_field,
        is_async=is_async,
        email_is_required=email_is_required,
        phone_is_required=phone_is_required,
        username_is_required=username_is_required,
        verification_enabled=verification_enabled,
    )


def configure_db_models_in_project(
    base_path: Path,
    auth_model: str,
    login_field: str | None,
    is_async: bool,
    email_is_required: bool,
    phone_is_required: bool,
    username_is_required: bool,
    verification_enabled: bool,
):
    """
    Configure database models in the project.

    This function generates the database models code and writes it to a file
    in the project directory.

    Args:
        base_path (Path): The base path of the project directory.
        auth_model (str): The name of the authentication model.
        login_field (str): The field used for login (e.g., "email" or "username").
        is_async (bool): Whether the application is using asynchronous dependencies.
        email_is_required (bool): Whether the email field is required.
        phone_is_required (bool): Whether the phone field is required.
        username_is_required (bool): Whether the username field is required.
        verification_enabled (bool): Whether email verification is enabled.
    """
    db_models_path = base_path / "app" / "db" / "models.py"
    print(f"[yellow]Configuring database models in {db_models_path}...[/yellow]")
    write_file(
        db_models_path,
        generate_db_models_code(
            auth_model=auth_model,
            login_field=login_field,
            is_async=is_async,
            email_is_required=email_is_required,
            phone_is_required=phone_is_required,
            username_is_required=username_is_required,
            verification_enabled=verification_enabled,
        ),
    )
    print("[green]Database models configured successfully![/green]")
