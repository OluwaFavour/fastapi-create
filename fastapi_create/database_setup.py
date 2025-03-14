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
    """Validate SQLite database URL (file path or :memory:)."""
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
    """Validate database connection details for non-SQLite engines with optional port."""
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


def configure_database() -> tuple[str | None, str, str]:
    """Configure the database connection details."""
    db_thread_type = Prompt.ask(
        "Do you want to set up an asynchronous database or synchronous database?",
        default="async",
        choices=["async", "sync"],
        show_choices=True,
    )
    db_engine = Prompt.ask(
        "Which database are you using?",
        default="postgresql",
        choices=["postgresql", "mysql", "sqlite", "mariadb"],
        show_choices=True,
    )
    db_dependency = {
        "postgresql": "psycopg",
        "mysql": "pymysql" if db_thread_type == "sync" else "asyncmy",
        "mariadb": "pymysql" if db_thread_type == "sync" else "asyncmy",
        "sqlite": "aiosqlite" if db_thread_type == "async" else None,
    }[db_engine]
    if db_engine == "sqlite":
        db_url = recursive_prompt_with_validation(
            prompt="Enter the path to the SQLite database file",
            error_msg="Invalid SQLite URL",
            validation_func=validate_sqlite_url,
        )
        db_url = (
            f"sqlite{'+aiosqlite' if db_thread_type == 'async' else ''}:///{db_url}"
        )
    else:

        def recursive_prompt():
            db_url = Prompt.ask(
                "Enter the database connection details (e.g., user:password@host:port/dbname)"
            )
            # Validate database URL
            if not validate_db_url(db_url, db_engine):
                print("[red]Invalid database URL[/red]")
                return recursive_prompt()

        db_url = recursive_prompt_with_validation(
            prompt="Enter the database connection details (e.g., user:password@host:port/dbname)",
            error_msg="Invalid database URL",
            validation_func=validate_db_url,
            validation_args=(db_engine,),
        )
        prefix = {
            "postgresql": "postgresql+psycopg",
            "mysql": f"mysql+{'asyncmy' if db_thread_type == 'async' else 'pymysql'}",
            "mariadb": f"mysql+{'asyncmy' if db_thread_type == 'async' else 'pymysql'}",
        }[db_engine]
        db_url = f"{prefix}://{db_url}"
    return db_dependency, db_url, db_thread_type


def configure_database_connection(
    db_dependency: str | None, db_url: str, base_path: Path
) -> None:
    """Write database connection details to .env and install dependency."""
    add_key_value_to_env_file(base_path / ".env", "DATABASE_URL", db_url)
    if db_dependency:
        print(f"[yellow]Installing database dependency {db_dependency}...[/yellow]")
        try:
            subprocess.run(["pip", "install", db_dependency], check=True)
        except subprocess.CalledProcessError:
            print(f"[red]Error installing {db_dependency}[/red]", file="stderr")
            raise RuntimeError(f"Error installing {db_dependency}")


def configure_database_in_project(db_thread_type: str, base_path: Path) -> None:
    """Configure database-related files in the project."""
    db_path = base_path / "app" / "db"
    configs: list[tuple[str, str, dict]] = [
        (
            "db_config_template.py.jinja2",
            "config.py",
            {"is_async": db_thread_type == "async"},
        ),
        (
            "init_db_template.py.jinja2",
            "init_db.py",
            {"is_async": db_thread_type == "async"},
        ),
        ("models_template.py.jinja2", "models.py", {}),
    ]
    for template_name, filename, kwargs in configs:
        print(f"[yellow]Writing {filename} to the project...[/yellow]")
        content = generate_file_content(template_name, **kwargs)
        write_file(db_path / filename, content)
        print(f"[green]{filename} written successfully[/green]")
