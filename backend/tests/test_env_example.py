"""Test environment variables template."""
from pathlib import Path


def test_env_example_exists():
    """Test that .env.example exists."""
    backend_path = Path(__file__).parent.parent
    env_example = backend_path / ".env.example"
    assert env_example.exists(), ".env.example should exist in backend/"


def test_env_example_has_required_vars():
    """Test that .env.example has required environment variables."""
    backend_path = Path(__file__).parent.parent
    env_example = backend_path / ".env.example"

    if env_example.exists():
        content = env_example.read_text()

        required_vars = [
            "APP_NAME",
            "DEBUG",
            "ENVIRONMENT",
            "DATABASE_URL",
            "SECRET_KEY",
        ]

        for var in required_vars:
            assert var in content, f".env.example should have {var} variable"


def test_env_example_has_comments():
    """Test that .env.example has helpful comments."""
    backend_path = Path(__file__).parent.parent
    env_example = backend_path / ".env.example"

    if env_example.exists():
        content = env_example.read_text()
        assert "#" in content, ".env.example should have comments to help users"
