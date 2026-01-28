# Publishing Your Package to PyPI

A step-by-step guide to publish **nexus-ai-search** to Python Package Index (PyPI)

## 📋 Prerequisites

Before publishing, make sure you have:

1. ✅ A [PyPI Account](https://pypi.org/account/register/)
2. ✅ A [Test PyPI Account](https://test.pypi.org/account/register/) (recommended for testing)
3. ✅ Python 3.8+ installed
4. ✅ Build tools installed

## 🔧 Step 1: Install Build Tools

Open PowerShell and run:

```powershell
pip install --upgrade pip setuptools wheel twine build
```

This installs:
- **setuptools** - Package building
- **wheel** - Binary package format
- **twine** - PyPI upload tool
- **build** - Modern build system

## 📁 Step 2: Prepare Your Package

Your package structure should look like this:

```
nexus-ai-search/
├── pyproject.toml          ✅ Created
├── setup.py                ✅ Exists
├── README.md               ✅ Exists
├── LICENSE                 ✅ Exists
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── ...
├── frontend/
│   ├── index.html
│   └── ...
└── .gitignore
```

Verify your package info is correct in `pyproject.toml`:
- ✅ Project name: `nexus-ai-search`
- ✅ Version: `1.0.0`
- ✅ Description is clear
- ✅ Author name and email
- ✅ GitHub URL

## 🏗️ Step 3: Build Your Package

Navigate to your project directory:

```powershell
cd "c:\Users\shaik\OneDrive\Desktop\Ai engine"
```

Build the package:

```powershell
python -m build
```

This creates:
- `dist/nexus_ai_search-1.0.0-py3-none-any.whl` (wheel)
- `dist/nexus-ai-search-1.0.0.tar.gz` (source distribution)

Verify the build succeeded - you should see these files in the `dist/` folder.

## 🧪 Step 4 (Optional): Test on TestPyPI

Before publishing to the real PyPI, test on TestPyPI:

```powershell
twine upload --repository testpypi dist/*
```

When prompted:
- **Username**: `__token__`
- **Password**: Your TestPyPI API token

After uploading, test installing it:

```powershell
pip install --index-url https://test.pypi.org/simple/ nexus-ai-search
```

## 📤 Step 5: Create PyPI API Token

1. Go to https://pypi.org/account/
2. Click **Account settings**
3. Go to **API tokens**
4. Click **Add API token**
5. Name it: `nexus-ai-search`
6. Scope: Select **Entire account**
7. Click **Create token**
8. **Copy the entire token** (starts with `pypi-`)

## 🔐 Step 6: Create .pypirc Configuration File

Create a `.pypirc` file in your home directory:

**On Windows:**
```
C:\Users\<YourUsername>\.pypirc
```

**File content:**
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_API_TOKEN_HERE
```

**Replace `YOUR_API_TOKEN_HERE` with your actual token!**

## 🚀 Step 7: Publish to PyPI

From your project directory:

```powershell
twine upload dist/*
```

When prompted:
- **Username**: `__token__`
- **Password**: Your PyPI API token (paste it)

Or use the `.pypirc` configuration (automatic):

```powershell
twine upload --repository pypi dist/*
```

## ✅ Step 8: Verify Your Package

After successful upload, check:

1. Visit: **https://pypi.org/project/nexus-ai-search/**
2. Your package should be visible
3. Version 1.0.0 should be listed
4. README should display correctly
5. Download files should be available

## 🎯 Step 9: Install from PyPI

Now anyone can install your package:

```bash
pip install nexus-ai-search
```

Or install with development dependencies:

```bash
pip install nexus-ai-search[dev]
```

## 📝 Version Management for Future Releases

When you make updates:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

2. **Update CHANGELOG** (optional but recommended)

3. **Create a Git tag**:
   ```powershell
   git tag v1.0.1
   git push origin v1.0.1
   ```

4. **Rebuild and upload**:
   ```powershell
   python -m build
   twine upload dist/*
   ```

## 🐛 Troubleshooting

### Issue: "Invalid distribution"
- **Solution**: Check your `setup.py` and `pyproject.toml` syntax
- Run: `python setup.py check`

### Issue: "File already exists"
- **Solution**: PyPI doesn't allow re-uploading the same version
- Update your version number in `pyproject.toml`
- Rebuild: `python -m build`

### Issue: "Invalid authentication"
- **Solution**: Check your API token
- Make sure password is the full token (starts with `pypi-`)
- Don't copy extra spaces

### Issue: "README not displaying"
- **Solution**: Check README format (must be valid Markdown)
- Run: `twine check dist/*`

## 📚 Useful Commands

```powershell
# Check your package metadata
twine check dist/*

# View package info
python -c "from setup import *; print(setup_args)"

# Dry run (without uploading)
twine upload --dry-run dist/*

# Upload with verbose output
twine upload -v dist/*

# List available distributions
Get-ChildItem dist/
```

## 🎉 Your Package is Live!

Once published, your package can be installed with:

```bash
pip install nexus-ai-search
```

Users can then:
- View it on PyPI: https://pypi.org/project/nexus-ai-search/
- Install it easily with pip
- Find your GitHub repository
- Report issues and contribute

## 📖 PyPI Package Page

Your package will have:
- ✅ Description and README
- ✅ Installation instructions
- ✅ Project links (GitHub, bug tracker)
- ✅ License information
- ✅ Download statistics
- ✅ Release history
- ✅ Programming language (Python 3.8+)

## 💡 Tips for Success

1. **Keep version numbers semantic**: Use `MAJOR.MINOR.PATCH` (e.g., 1.0.0)
2. **Write good README**: This is what people see first
3. **Tag releases**: Tag each version in Git
4. **Update CHANGELOG**: Document what changed
5. **Test thoroughly**: Test on TestPyPI first
6. **Keep dependencies updated**: Periodically update `requirements.txt`
7. **Add badges**: Add PyPI badge to your GitHub README

## 🔗 Useful Links

- PyPI: https://pypi.org/
- Create Account: https://pypi.org/account/register/
- API Tokens: https://pypi.org/account/
- Twine Docs: https://twine.readthedocs.io/
- setuptools Docs: https://setuptools.pypa.io/

---

## Quick Summary

1. Install tools: `pip install build twine`
2. Build package: `python -m build`
3. Create PyPI account & API token
4. Upload: `twine upload dist/*`
5. Done! Package is live on PyPI

Your **nexus-ai-search** package is ready to share with the world! 🎉
