import os
from pathlib import Path
from rich import print
from rich.prompt import Prompt
import subprocess

from constants import DB_URL_REGEX
import typer
from utils import load_template, write_file, add_key_value_to_env_file


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
        "Should the database connection be async or sync?",
        default="async",
        choices=["async", "sync"],
        show_choices=True,
    )
    db_engine = Prompt.ask(
        "Which database engine would you like to use?",
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
        db_url = Prompt.ask("Enter the path to the SQLite database file")
        # Validate SQLite URL
        if not validate_sqlite_url(db_url):
            raise typer.Exit(code=1)
        db_url = (
            f"sqlite{'+aiosqlite' if db_thread_type == 'async' else ''}:///{db_url}"
        )
    else:
        db_url = Prompt.ask(
            "Enter the database connection details (e.g., user:password@host:port/dbname)"
        )
        # Validate database URL
        if not validate_db_url(db_url, db_engine):
            raise typer.Exit(code=1)
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
            raise typer.Exit(code=1)


def generate_database_configuration_code(db_thread_type: str) -> str:
    """Generate database configuration code from a template."""
    print("[yellow]Generating database configuration code...[/yellow]")
    template_name = (
        f"{'sync' if db_thread_type == 'sync' else 'async'}_db_config_template.py"
    )
    return load_template(template_name)


def generate_init_db_code(db_thread_type: str) -> str:
    """Generate database initialization code from a template."""
    print("[yellow]Generating database initialization code...[/yellow]")
    template_name = (
        f"{'sync' if db_thread_type == 'sync' else 'async'}_init_db_template.py"
    )
    return load_template(template_name)


def generate_models_code() -> str:
    """Generate models code from a template."""
    print("[yellow]Generating models code...[/yellow]")
    return load_template("models_template.py")


def configure_database_in_project(db_thread_type: str, base_path: Path) -> None:
    """Configure database-related files in the project."""
    db_path = base_path / "app" / "db"
    for name, generator in [
        ("config.py", generate_database_configuration_code),
        ("init_db.py", generate_init_db_code),
        ("models.py", generate_models_code),
    ]:
        print(f"[yellow]Writing {name} to the project...[/yellow]")
        content = generator(db_thread_type) if "models" not in name else generator()
        write_file(db_path / name, content)
        print(f"[green]{name} written successfully[/green]")
