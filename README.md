# fastapi-create

A command-line tool to quickly scaffold a FastAPI project with pre-configured database support, migrations, and essential setup files.

## Features

- **Project Structure Creation**: Generates a clean, organized FastAPI project layout.
- **Database Configuration**: Supports both synchronous (e.g., SQLAlchemy) and asynchronous (e.g., asyncpg) database setups.
- **Alembic Integration**: Sets up Alembic for database migrations with a customizable folder name.
- **Dependency Management**: Automatically installs required dependencies based on your database choice.
- **Configuration Files**: Creates core configuration files and a `.env` for environment variables.
- **Main Application Setup**: Generates a `main.py` tailored to your database threading choice.
- **Utility Scripts**: Adds a `manage.py` for project management tasks.
- **Documentation**: Includes a basic `README.md` and `requirements.txt` in the generated project.

*Planned Features (Coming Soon):*

- Support for additional database engines (e.g., MongoDB).
- Pre-built API route templates.
- Testing framework integration (e.g., pytest).

## Installation

*Ensure you have Python 3.8+ installed.*

- Create a new virtual environment:

```bash
python -m venv venv
```

- Activate the virtual environment:

- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

- Upgrade pip

```bash
python -m pip install --upgrade pip
```

- Install `fastapi-create` globally using pip:

```bash
pip install fastapi-create
```

## Usage

To create a new FastAPI project, run:

```bash
fastapi-create my_project
```

### What Happens Next?

1. **Project Name Validation**: Ensures your project name is valid (e.g., no special characters).
2. **Database Setup**: Prompts you to choose a database dependency (e.g., SQLAlchemy, asyncpg) and provide a database URL.
3. **Alembic Configuration**: Asks for a folder name for Alembic migrations (defaults to alembic if unspecified).
4. **Project Generation**: Sets up the project structure, installs dependencies, and configures all necessary files.

Examples:

- Generates the project in the current working directory.

```bash
fastapi-create .
Do you want to set up an asynchronous database or synchronous database? [async/sync] (async): async
Which database are you using? [postgresql/mysql/sqlite/mariadb] (postgresql): sqlite
Enter the path to the SQLite database file: :memory:
Enter the name of the Alembic folder (alembic): migrations
```

- Generates the project in a directory called test-project relative to the current working directory.

```bash
fastapi-create test-project
Do you want to set up an asynchronous database or synchronous database? [async/sync] (async): async
Which database are you using? [postgresql/mysql/sqlite/mariadb] (postgresql): sqlite
Enter the path to the SQLite database file: :memory:
Enter the name of the Alembic folder (alembic): migrations
```

- Calling `fastapi-create [PATH]` without the `[PATH]` prompts the user for a project name.

```bash
fastapi-create
Enter the project name: test-project
Do you want to set up an asynchronous database or synchronous database? [async/sync] (async): async
Which database are you using? [postgresql/mysql/sqlite/mariadb] (postgresql): sqlite
Enter the path to the SQLite database file: :memory:
Enter the name of the Alembic folder (alembic): migrations
```

## Generated Project Structure

After running the command, your project will look like this:

```text
my_project/
├── app/
│   ├── core/
│   │   ├── config.py      # Core configuration (e.g., environment variables)
│   │   └── __init__.py
│   ├── db/
│   │   ├── config.py      # Database connection setup
│   │   ├── init_db.py     # Database initialization
│   │   ├── models.py      # Database models
│   │   └── __init__.py
│   ├── routes/            # API routes (to be expanded)
│   │   └── __init__.py
│   ├── schemas/           # Pydantic schemas (to be expanded)
│   │   └── __init__.py
│   ├── main.py            # FastAPI app entry point
│   └── __init__.py
├── migrations/            # Alembic migrations folder (name customizable)
├── .env                   # Environment variables (e.g., DATABASE_URL)
├── manage.py             # Management script
├── README.md             # Project-specific README
└── requirements.txt      # Project dependencies
```

## Configuration

Edit the .env file in your generated project to customize settings, such as:

```text
DATABASE_URL=sqlite:///my_project.db
```

## Contributing

We’d love for the FastAPI community to help improve fastapi-create! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get involved.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- FastAPI - The amazing web framework powering this tool.
- Alembic - For database migration support.
- Typer - For building the CLI interface.

## Contact

Questions or feedback? Reach out via [email](mailto:fsticks8187@gmail.com) or [GitHub - OluwaFavour](https://github.com/OluwaFavour).
