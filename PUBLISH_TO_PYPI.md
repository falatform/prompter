# Step-by-step: PyPI Trusted Publisher Setup for GitHub Actions

1. **Register on PyPI**
   - Go to https://pypi.org/account/register/ and create an account.

2. **Create your PyPI project**
   - Log in to PyPI.
   - Click "Add Project" and reserve your project name (e.g., `prompter`).

3. **Link your GitHub repo to PyPI (Trusted Publisher)**
   - Go to your PyPI account settings → "Trusted Publishers".
   - Click "Add a publisher" → "GitHub Actions".
   - Fill in:
     - **Owner**: `falatform`
     - **Repository name**: `prompter`
     - **Workflow name**: `publish-to-pypi.yml` (or leave blank for any workflow)
   - Save and copy the "PyPI project" name (should match your package name).

4. **Push your code and workflow to GitHub**
   - Make sure your `pyproject.toml`, code, and `.github/workflows/publish-to-pypi.yml` are committed and pushed.

5. **Run the GitHub Action**
   - Go to your repo's "Actions" tab.
   - Find the "Publish Python 🐍 distribution to PyPI" workflow.
   - Click "Run workflow" (manual trigger).

6. **Check PyPI**
   - After the workflow completes, your package should be live on https://pypi.org/project/prompter/

---

**You do NOT need to set any PyPI password or token in GitHub secrets.**

For more details, see: https://docs.pypi.org/trusted-publishers/using-a-publisher/
