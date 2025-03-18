from rich.prompt import Prompt
from fastapi_create.utils import recursive_prompt_with_validation


def validate_auth_required_fields(required_fields: str) -> bool:
    """
    Validate the required fields for authentication.

    The function checks if the required fields for authentication are valid.

    Args:
        required_fields (str): The required fields for authentication.

    Returns:
        bool: A boolean indicating whether the required fields are valid.
    """
    return all(
        field.strip() in ["email", "username", "phone"]
        for field in required_fields.split(",")
    )


def clean_auth_required_fields(required_fields: str) -> set[str]:
    """
    Clean the required fields for authentication.

    The function cleans the required fields for authentication.

    Args:
        required_fields (str): The required fields for authentication.

    Returns:
        set[str]: The cleaned required fields for authentication.
    """
    return {field.strip() for field in required_fields.split(",")}


def validate_auth_model(auth_model: str) -> bool:
    """
    Validate the authentication model.

    The function checks if the authentication model is valid.

    Args:
        auth_model (str): The authentication model.

    Returns:
        bool: A boolean indicating whether the authentication model is valid.
    """
    return auth_model.isidentifier()


def handle_auth_setup():

    # Prompt user for Auth configuration
    auth_model = recursive_prompt_with_validation(
        prompt="Enter the name of the authentication model",
        validation_func=validate_auth_model,
        prompt_kwargs={"default": "User"},
    )
    required_fields = recursive_prompt_with_validation(
        prompt="Which fields are required for signup? (Choose a comma-separated list of 'email', 'username', 'phone')",
        validation_func=validate_auth_required_fields,
        prompt_kwargs={"default": "email"},
    )
    required_fields = clean_auth_required_fields(required_fields)
    login_field = Prompt.ask(
        "Which field should be used for login?",
        choices=list(required_fields),
    )

    return auth_model, required_fields, login_field
