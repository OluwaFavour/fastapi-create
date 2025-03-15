import re


# CONSTANTS

## Regular expression to validate project names
PROJECT_NAME_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_-]*$")
## Regex for validating non-SQLite database connection details
DB_URL_REGEX = re.compile(
    r"^[a-zA-Z0-9_]+:[^@]+@[a-zA-Z0-9.-]+(?::[0-9]{1,5})?/[a-zA-Z0-9_]+(?:\?.*)?$"
)
## Regex for validating SMTP server details
SMTP_HOST_REGEX = re.compile(
    r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
)
SMTP_PORT_REGEX = re.compile(r"^[1-9][0-9]{0,4}$")
SMTP_USERNAME_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
)

## Dependencies to install
DEPENDENCIES = [
    "fastapi[all]",
    "pydantic-settings",
    "pydantic-extra-types",
    "alembic",
    "passlib[bcrypt]",
]
