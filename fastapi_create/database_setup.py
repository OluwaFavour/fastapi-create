import os
from pathlib import Path
from rich import print
from rich.prompt import Prompt
import subprocess

from fastapi_create.constants import DB_URL_REGEX
import typer
from fastapi_create.utils import (
    generate_file_content,
    recursive_prompt_with_validation,
    write_file,
    add_key_value_to_env_file,
)


def validate_sqlite_url(value: str) -> bool:
    """
    Validate SQLite database URL (file path or :memory:).

    This function checks if the provided SQLite database URL is valid. It accepts
    either a special ":memory:" string for an in-memory database or a file path.
    For file paths, it verifies that the directory exists and is writable.

    Args:
        value (str): The SQLite database URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    if value == ":memory:":
        return True
    path = Path(value)
    try:
        if (
            path.parent.exists()
            and path.parent.is_dir()
            and os.access(path.parent, os.W_OK)
        ):
            return True
        print(
            f"[red]Error: Directory {path.parent} is not writable or does not exist[/red]"
        )
        return False
    except Exception as e:
        print(f"[red]Error validating SQLite path: {e}[/red]")
        return False


def validate_db_url(value: str, engine: str) -> bool:
    """
    Validate database connection details for non-SQLite engines with optional port.

    Args:
        value (str): The database URL to validate.
        engine (str): The name of the database engine (e.g., PostgreSQL, MySQL).

    Returns:
        bool: True if the URL is valid, False otherwise.

    The function checks if the provided database URL matches the expected format:
    'user:password@host[:port]/dbname'. It also ensures that the port number, if provided,
    is within the valid range (1-65535). If the URL is malformed or does not meet the
    criteria, an error message is printed and the function returns False.
    """
    if not DB_URL_REGEX.match(value):
        print(
            f"[red]Error: Invalid format for {engine}. Expected: user:password@host[:port]/dbname[/red]"
        )
        return False
    try:
        user_pass, rest = value.split("@", 1)
        host_port_dbname = rest.split("/", 1)
        if len(host_port_dbname) != 2:
            print(f"[red]Error: Missing database name after '/'[/red]")
            return False
        host_port, dbname = host_port_dbname
        if ":" in host_port:
            host, port = host_port.split(":", 1)
            if not (1 <= int(port) <= 65535):
                print(f"[red]Error: Port {port} must be between 1 and 65535[/red]")
                return False
        return True
    except ValueError:
        print(f"[red]Error: Malformed URL for {engine}[/red]")
        return False


def configure_database(is_async: bool) -> tuple[str | None, str]:
    """
    Configure the database connection details.

    Prompts the user to select the database engine (PostgreSQL, MySQL, SQLite, or MariaDB). Based on the
    user's choices, it determines the appropriate database dependency and constructs
    the database URL.

    Args:
        is_async (bool): A boolean indicating whether the database should be asynchronous

    Returns:
        tuple: A tuple containing:
            - db_dependency (str | None): The database dependency module name.
            - db_url (str): The constructed database connection URL.
    """
    db_engine = Prompt.ask(
        "Which database are you using?",
        default="postgresql",
        choices=["postgresql", "mysql", "sqlite", "mariadb"],
        show_choices=True,
    )
    db_dependency = {
        "postgresql": "psycopg",
        "mysql": "pymysql" if not is_async else "asyncmy",
        "mariadb": "pymysql" if not is_async else "asyncmy",
        "sqlite": "aiosqlite" if is_async else None,
    }[db_engine]
    if db_engine == "sqlite":
        db_url = recursive_prompt_with_validation(
            prompt="Enter the path to the SQLite database file",
            validation_func=validate_sqlite_url,
        )
        db_url = f"sqlite{'+aiosqlite' if is_async else ''}:///{db_url}"
    else:
        db_url = recursive_prompt_with_validation(
            prompt="Enter the database connection details (e.g., user:password@host:port/dbname)",
            validation_func=validate_db_url,
            validation_args=(db_engine,),
        )
        prefix = {
            "postgresql": "postgresql+psycopg",
            "mysql": f"mysql+{'asyncmy' if is_async else 'pymysql'}",
            "mariadb": f"mysql+{'asyncmy' if is_async else 'pymysql'}",
        }[db_engine]
        db_url = f"{prefix}://{db_url}"
    return db_dependency, db_url


def configure_database_connection(db_url: str, base_path: Path) -> None:
    """
    Write database connection details to a .env file.

    This function takes a database URL and a base path, and writes the database
    connection details to a .env file located at the specified base path.

    Args:
        db_url (str): The database connection URL.
        base_path (Path): The base path where the .env file is located.

    Returns:
        None
    """
    add_key_value_to_env_file(base_path / ".env", "DATABASE_URL", db_url)


def configure_database_in_project(is_async: bool, base_path: Path) -> None:
    """
    Configure database-related files in the project.

    This function sets up the necessary database configuration files in the specified project directory.
    It uses Jinja2 templates to generate the content of these files based on the provided database thread type.

    Args:
        is_async (bool): A boolean indicating whether the database should be asynchronous.
        base_path (Path): The base path of the project where the database configuration files will be created.

    Returns:
        None
    """
    db_path = base_path / "app" / "db"
    configs: list[tuple[str, str, dict]] = [
        (
            "db_config_template.py.jinja2",
            "config.py",
            {"is_async": is_async},
        ),
        (
            "init_db_template.py.jinja2",
            "init_db.py",
            {"is_async": is_async},
        ),
        ("models_template.py.jinja2", "models.py", {}),
    ]
    for template_name, filename, kwargs in configs:
        print(f"[yellow]Writing {filename} to the project...[/yellow]")
        content = generate_file_content(template_name, **kwargs)
        write_file(db_path / filename, content)
        print(f"[green]{filename} written successfully[/green]")
