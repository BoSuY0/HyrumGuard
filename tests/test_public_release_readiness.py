from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_project_urls_point_to_public_repository():
    pyproject = (ROOT / "pyproject.toml").read_text()

    assert "https://github.com/BoSuY0/HyrumGuard" in pyproject
    assert 'Homepage = "https://github.com/BoSuY0/HyrumGuard"' in pyproject
    assert 'Source = "https://github.com/BoSuY0/HyrumGuard"' in pyproject
    assert 'Issues = "https://github.com/BoSuY0/HyrumGuard/issues"' in pyproject


def test_public_release_docs_name_github_release_channel():
    readme = (ROOT / "README.md").read_text()
    release_doc = (ROOT / "docs" / "reference" / "release.md").read_text()
    control = (ROOT / "CONTROL.md").read_text()

    assert "https://github.com/BoSuY0/HyrumGuard" in readme
    assert "v1.0.0" in release_doc
    assert "gh release view v1.0.0 --repo BoSuY0/HyrumGuard" in release_doc
    assert "Public repository: `BoSuY0/HyrumGuard`" in control
    assert "Do not claim PyPI" in release_doc


def test_release_workflow_builds_checks_and_uploads_public_assets():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text()

    assert "on:" in workflow
    assert "tags:" in workflow
    assert "v*" in workflow
    assert "python -m build" in workflow
    assert "twine check dist/*" in workflow
    assert "softprops/action-gh-release" in workflow
    assert "dist/hyrumguard-*.tar.gz" in workflow
    assert "dist/hyrumguard-*-py3-none-any.whl" in workflow
    assert "pypa/gh-action-pypi-publish" in workflow


def test_release_plan_requires_public_verification():
    goal = (ROOT / "GOAL.md").read_text()
    plan = (ROOT / "PLAN.md").read_text()

    assert "gh repo view BoSuY0/HyrumGuard" in goal
    assert "gh release view v1.0.0 --repo BoSuY0/HyrumGuard" in goal
    assert "Verify public repo/release/assets from GitHub" in plan
