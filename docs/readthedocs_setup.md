# Read the Docs Setup Guide

This guide explains how to set up Sagely documentation on Read the Docs.

## Prerequisites

1. A GitHub repository with the Sagely code
2. A Read the Docs account (free at https://readthedocs.org/)

## Setup Steps

### 1. Connect Your Repository

1. Go to https://readthedocs.org/
2. Sign in with your GitHub account
3. Click "Import a Project"
4. Select your Sagely repository
5. Click "Import"

### 2. Configure Build Settings

In your Read the Docs project settings:

1. **Build Configuration**: Set to `docs/requirements.txt`
2. **Python Interpreter**: Choose Python 3.8 or higher
3. **Install Project**: Set to "Install your project inside a virtualenv using setup.py install"
4. **Conf File**: Set to `docs/conf.py`

### 3. Environment Variables

Set these environment variables in your Read the Docs project settings:

- `OPENAI_API_KEY`: Your OpenAI API key (for building examples)
- `TAVILY_API_KEY`: Your Tavily API key (optional)
- `LANGCHAIN_API_KEY`: Your LangSmith API key (optional)

### 4. Build Configuration

The documentation is configured to build automatically with:

- **Requirements File**: `docs/requirements.txt`
- **Configuration File**: `docs/conf.py`
- **Documentation Type**: Sphinx HTML

### 5. Version Settings

Configure version settings:

- **Default Version**: Set to `latest` or `main`
- **Default Branch**: Set to `main`
- **Version Privacy**: Choose based on your needs

## Build Process

Read the Docs will automatically:

1. Clone your repository
2. Install dependencies from `docs/requirements.txt`
3. Install your project in development mode
4. Build the documentation using Sphinx
5. Deploy the built documentation

## Custom Domain (Optional)

You can set up a custom domain:

1. Go to your project settings
2. Navigate to "Domains"
3. Add your custom domain (e.g., `docs.sagely.ai`)
4. Configure DNS as instructed

## Troubleshooting

### Build Failures

Common issues and solutions:

1. **Import Errors**: Make sure your project is installed correctly
2. **Missing Dependencies**: Check `docs/requirements.txt`
3. **Configuration Errors**: Verify `docs/conf.py` syntax
4. **Path Issues**: Ensure `sys.path` is set correctly in `conf.py`

### Environment Variables

If you need environment variables for the build:

1. Go to project settings
2. Navigate to "Environment Variables"
3. Add required variables
4. Mark as "Public" if needed for the build

### Build Logs

Check build logs for detailed error information:

1. Go to your project on Read the Docs
2. Click on "Builds"
3. Click on a specific build
4. View the build log for errors

## Maintenance

### Updating Documentation

1. Make changes to your documentation
2. Commit and push to your repository
3. Read the Docs will automatically rebuild
4. Check the build status and logs

### Version Management

- **Stable**: Tagged releases
- **Latest**: Main branch
- **Pre-release**: Development branches

### Monitoring

Monitor your documentation:

1. Check build status regularly
2. Review build logs for warnings
3. Test links and examples
4. Update dependencies as needed

## Best Practices

1. **Keep Dependencies Updated**: Regularly update `docs/requirements.txt`
2. **Test Locally**: Build documentation locally before pushing
3. **Use Version Control**: Tag releases for stable documentation
4. **Monitor Builds**: Check build status after each push
5. **Document Changes**: Keep changelog updated

## Resources

- [Read the Docs Documentation](https://docs.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [MyST Parser Documentation](https://myst-parser.readthedocs.io/)
- [Read the Docs Support](https://readthedocs.org/support/) 