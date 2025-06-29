# sagely Package Release Guide

This guide explains how to prepare and release the sagely package to PyPI.

## Prerequisites

1. **PyPI Account**: You need a PyPI account to upload packages
2. **TestPyPI Account**: Recommended for testing releases
3. **Required Tools**: Install the following packages:
   ```bash
   pip install build twine
   ```

## Package Structure

The sagely package uses a modern Python packaging structure:

```
sagely/
├── src/sagely/           # Source code
├── tests/              # Test files
├── pyproject.toml      # Package configuration
├── MANIFEST.in         # Files to include in distribution
├── LICENSE.md          # MIT License
├── README.md           # Package documentation
├── release.py          # Release automation script
└── RELEASE.md          # This file
```

## Release Process

### 1. Update Version

Before releasing, update the version in `pyproject.toml`:

```toml
[project]
name = "sagely"
version = "0.0.2"  # Increment this
```

### 2. Build the Package

Use the release script to build the package:

```bash
python release.py build
```

This will:
- Clean previous build artifacts
- Build both source distribution (`.tar.gz`) and wheel (`.whl`)
- Create files in the `dist/` directory

### 3. Test the Build

Check that the package builds correctly:

```bash
python release.py check
```

### 4. Test Installation

Test that the built package can be installed:

```bash
pip install dist/sagely-0.0.1-py3-none-any.whl --force-reinstall
python -c "import sagely; print('Success!')"
```

### 5. Upload to TestPyPI (Recommended)

First, test the upload to TestPyPI:

```bash
python release.py test-upload
```

You'll need to provide your TestPyPI credentials when prompted.

### 6. Upload to PyPI

Once tested, upload to the main PyPI:

```bash
python release.py upload
```

You'll need to provide your PyPI credentials when prompted.

## Manual Commands

If you prefer to run commands manually:

```bash
# Clean build artifacts
rm -rf build/ dist/ src/sagely.egg-info/

# Build package
python -m build

# Check package
python -m build --check

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## Package Configuration

The package is configured in `pyproject.toml` with:

- **Modern packaging**: Uses `pyproject.toml` instead of `setup.py`
- **Source layout**: Code is in `src/sagely/` for better isolation
- **Dependencies**: All required packages with version constraints
- **Metadata**: Complete package information for PyPI
- **License**: MIT license using SPDX format
- **Classifiers**: Comprehensive PyPI classifiers for discoverability

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure the package is installed in development mode:
   ```bash
   pip install -e .
   ```

2. **Build Errors**: Check that all required files are present:
   - `pyproject.toml`
   - `MANIFEST.in`
   - `LICENSE.md`
   - `README.md`
   - All Python files in `src/sagely/`

3. **Upload Errors**: Ensure you have the correct credentials and permissions

### Version Conflicts

If you get version conflicts during installation, the package is working correctly - it's just that other packages in your environment have conflicting dependencies.

## Next Steps

After a successful release:

1. **Update Documentation**: Update any version references in documentation
2. **Create Release Notes**: Document what changed in this version
3. **Test Installation**: Test the package installation from PyPI
4. **Monitor**: Check that the package appears correctly on PyPI

## Security Notes

- Never commit API keys or credentials
- Use environment variables for sensitive data
- Test thoroughly before releasing to main PyPI
- Consider using TestPyPI for all testing 