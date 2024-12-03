# Contributing to the Multilingual IR System

We welcome contributions from the community. To ensure a smooth collaboration, please follow these guidelines when contributing to this project.

## Getting Started

- **Fork** the repository on GitHub.
- **Clone** your forked repository to your local machine.
  ```bash
  git clone https://github.com/your_username/lapair.git
  ```
- **Create a Branch** for your feature or bug fix.
  ```bash
  git checkout -b feature/your-feature-name
  ```

## Coding Standards

### C++ Code

- Follow the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
- Use `clang-format` for code formatting.
- Use `clang-tidy` for static code analysis.
- Write clear, consistent, and well-documented code.
- Aim for modularity and maintainability.

### Python Code

- Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
- Use `pylint` or `flake8` for linting.
- Include type annotations where appropriate.
- Keep functions and classes small and focused.

## Commit Guidelines

- Write clear and descriptive commit messages.
- Use the present tense (e.g., "Add feature" not "Added feature").
- Capitalize the first letter of the commit message.
- Reference issue numbers when applicable (e.g., `Fixes #123`).

## Pull Request Process

1. **Ensure Code Quality**

   - Run all unit tests and ensure they pass.
   - Verify that code complies with style guidelines and passes all linters.
   - Make sure pre-commit hooks are passing.

2. **Update Documentation**

   - Update `README.md` and other relevant documentation files if your changes affect them.
   - Document any new features or changes in behavior.

3. **Submit Pull Request**

   - Push your branch to GitHub.
     ```bash
     git push origin feature/your-feature-name
     ```
   - Open a pull request against the `main` branch.
   - Fill out the pull request template, providing as much detail as possible.
   - Be prepared to engage in the code review process, making changes as requested.

## Code Review

- Be open to feedback and willing to make necessary changes.
- Discuss any significant architectural decisions.
- Maintain respectful and constructive communication.

## Issue Reporting

- Search existing issues before opening a new one to avoid duplicates.
- Provide a clear and descriptive title and detailed information.
- Include steps to reproduce the issue when applicable.

## Branching Model

- Use the GitFlow branching model.
  - `main`: Production-ready code.
  - `develop`: Latest development changes.
  - Feature branches: `feature/your-feature-name`
  - Bugfix branches: `bugfix/your-bugfix-name`

## Licensing

- By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Acknowledgments

- We appreciate your time and effort in contributing to this project.
- Thank you for helping improve the Multilingual IR System!
