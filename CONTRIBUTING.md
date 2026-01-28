# Contributing to Nexus AI Search Engine

First off, thank you for considering contributing to Nexus AI! It's people like you that make Nexus such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and the expected behavior**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* Include appropriate test cases
* Update the README.md with details of changes if applicable
* End all files with a newline

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🚀 `:rocket:` when improving performance
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - ✨ `:sparkles:` when implementing a new feature
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies

### Python Styleguide

All Python code should adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specifications:

* Use 4 spaces for indentation
* Maximum line length of 100 characters
* Use docstrings for all public modules, functions, classes, and methods
* Use type hints where applicable
* Use meaningful variable and function names

Example:
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    pass
```

### JavaScript Styleguide

* Use ES6 features when possible
* Use meaningful variable and function names
* Add comments for complex logic
* Use `const` by default, `let` when reassignment is needed

### Documentation Styleguide

* Use Markdown
* Reference other sections and files with links
* Include code examples when helpful

## Development Setup

1. Fork and clone the repository
2. Create a new branch for your feature/fix: `git checkout -b feature/your-feature-name`
3. Create a virtual environment: `python -m venv venv`
4. Activate it and install dependencies: `pip install -r backend/requirements.txt`
5. Make your changes
6. Test thoroughly
7. Commit with descriptive messages
8. Push to your fork
9. Create a Pull Request with a clear description

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested

## Recognition

Contributors will be recognized in the README.md file and in release notes.

---

Thank you for contributing! 🎉
