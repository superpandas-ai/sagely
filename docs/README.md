# Sagely Documentation

This directory contains the documentation for Sagely, built with Sphinx and hosted on Read the Docs.

## Building the Documentation

### Prerequisites

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Sagely in development mode:
   ```bash
   pip install -e ..
   ```

### Building Locally

1. Navigate to the docs directory:
   ```bash
   cd docs
   ```

2. Build the documentation:
   ```bash
   make html
   ```

3. View the documentation:
   ```bash
   # On Linux/macOS
   open _build/html/index.html
   
   # On Windows
   start _build/html/index.html
   ```

### Building for Read the Docs

The documentation is automatically built by Read the Docs when changes are pushed to the repository. The build process uses the `requirements.txt` file in this directory.

## Documentation Structure

- `index.rst` - Main documentation index
- `getting_started/` - Installation and basic usage
- `user_guide/` - Comprehensive usage guide
- `api_reference/` - Complete API documentation
- `configuration/` - Configuration options
- `examples/` - Real-world examples
- `advanced/` - Advanced topics
- `contributing/` - Contributing guidelines

## Adding New Documentation

1. Create a new `.rst` file in the appropriate directory
2. Add it to the `toctree` in the relevant `index.rst` file
3. Follow the existing documentation style
4. Build locally to test your changes
5. Commit and push your changes

## Documentation Style Guide

- Use clear, concise language
- Include code examples for all features
- Use admonitions for important notes, warnings, and tips
- Follow the existing formatting patterns
- Include cross-references to related sections
- Test all code examples

## Read the Docs Configuration

The documentation is configured for Read the Docs with:

- Sphinx as the documentation generator
- Read the Docs theme
- MyST Parser for Markdown support
- Copy button extension for code blocks
- Intersphinx for external references
- Custom CSS for styling

## Troubleshooting

### Build Errors

If you encounter build errors:

1. Check that all dependencies are installed
2. Verify that Sagely is installed in development mode
3. Check for syntax errors in RST files
4. Look for missing imports or references

### Import Errors

If you get import errors during the build:

1. Make sure you're in the correct Python environment
2. Verify that Sagely is installed: `python -c "import sagely"`
3. Check that the `sys.path` is set correctly in `conf.py`

### Styling Issues

If the documentation doesn't look right:

1. Check that the custom CSS is being loaded
2. Verify that the theme is set correctly in `conf.py`
3. Clear the build cache: `make clean`

## Contributing to Documentation

When contributing to the documentation:

1. Follow the existing style and structure
2. Include code examples that actually work
3. Test your changes locally before submitting
4. Update the table of contents if needed
5. Add appropriate cross-references

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Read the Docs Documentation](https://docs.readthedocs.io/)
- [MyST Parser Documentation](https://myst-parser.readthedocs.io/)
- [ReStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) 