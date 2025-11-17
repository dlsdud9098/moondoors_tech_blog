"""Test project documentation."""
from pathlib import Path


def test_readme_exists():
    """Test that README.md exists."""
    backend_path = Path(__file__).parent.parent
    readme = backend_path / "README.md"
    assert readme.exists(), "README.md should exist in backend/"


def test_readme_has_content():
    """Test that README.md has content."""
    backend_path = Path(__file__).parent.parent
    readme = backend_path / "README.md"

    if readme.exists():
        content = readme.read_text()
        assert len(content) > 100, "README.md should have meaningful content"


def test_readme_has_setup_instructions():
    """Test that README.md includes setup instructions."""
    backend_path = Path(__file__).parent.parent
    readme = backend_path / "README.md"

    if readme.exists():
        content = readme.read_text().lower()
        assert "setup" in content or "install" in content, \
            "README should include setup/installation instructions"


def test_readme_has_run_instructions():
    """Test that README.md includes how to run the application."""
    backend_path = Path(__file__).parent.parent
    readme = backend_path / "README.md"

    if readme.exists():
        content = readme.read_text().lower()
        assert "run" in content or "start" in content, \
            "README should include instructions to run the application"


def test_readme_has_test_instructions():
    """Test that README.md includes how to run tests."""
    backend_path = Path(__file__).parent.parent
    readme = backend_path / "README.md"

    if readme.exists():
        content = readme.read_text().lower()
        assert "test" in content or "pytest" in content, \
            "README should include testing instructions"
