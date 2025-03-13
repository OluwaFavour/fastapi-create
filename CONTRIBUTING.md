# Contributing to fastapi-create

Thank you for your interest in contributing to `fastapi-create`! I welcome contributions from the FastAPI community to make this tool even better.

## Getting Started

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/[your-username]/fastapi-create.git
   cd fastapi-create
   ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Development Environment**:
    - Ensure Python 3.8+ is installed.
    - No additional environment variables are required for development.

## Code Style

- Adhere to PEP 8 for Python code.
- Use type hints where possible (encouraged by FastAPI’s philosophy).
- Write clear, concise comments for complex logic.

## Submitting Changes

- **Fork the Repository**: Create your own fork on GitHub.
- **Create a Branch**:

    ```bash
    git checkout -b feature/your-feature-name
    ```

- **Make Changes**: Implement your feature or fix.
- **Test Your Changes**: Ensure your code works as expected (see Testing below).
- **Commit**: Use descriptive commit messages:

    ```bash
    git commit -m "Add feature: support for MongoDB integration"
    ```

- **Push: Upload your branch**:

    ```bash
        git push origin feature/your-feature-name
    ```

- **Submit a Pull Request**: Open a PR on the main repository with a detailed description of your changes.

## Testing

Currently, there’s no formal test suite (help us add one!). For now:

- Test manually by running fastapi-create create test_project and verifying the output.
- Ensure no errors occur during project generation.

Future contributions could include setting up pytest for automated testing.

## Documentation

- Update README.md or other files if your changes affect usage or features.
- Keep documentation clear and user-friendly.

## Code of Conduct

I aim to foster an inclusive community. Please be respectful and constructive in all interactions.

## Ideas for Contributions

- Add support for more database engines (e.g., MongoDB, PostgreSQL-specific features).
- Implement pre-built route templates.
- Integrate a testing framework.
- Enhance error handling or user prompts.

Questions? Reach out via [email](mailto:fsticks8187@gmail.com) or [open an issue on GitHub](https://github.com/OluwaFavour/fastapi-create/issues).
