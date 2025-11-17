"""Test pytest configuration."""
from pathlib import Path
import configparser


def test_pytest_ini_exists():
    """Test that pytest.ini exists."""
    backend_path = Path(__file__).parent.parent / "backend"
    pytest_ini = backend_path / "pytest.ini"
    assert pytest_ini.exists(), "pytest.ini should exist in backend/"


def test_pytest_ini_has_asyncio_mode():
    """Test that pytest.ini configures asyncio mode."""
    backend_path = Path(__file__).parent.parent / "backend"
    pytest_ini = backend_path / "pytest.ini"

    if pytest_ini.exists():
        config = configparser.ConfigParser()
        config.read(pytest_ini)

        assert "pytest" in config.sections(), "pytest.ini should have [pytest] section"
        assert "asyncio_mode" in config["pytest"], "pytest.ini should configure asyncio_mode"
        assert config["pytest"]["asyncio_mode"] == "auto", "asyncio_mode should be 'auto'"


def test_pyproject_toml_exists():
    """Test that pyproject.toml exists."""
    backend_path = Path(__file__).parent.parent / "backend"
    pyproject = backend_path / "pyproject.toml"
    assert pyproject.exists(), "pyproject.toml should exist in backend/"


def test_pyproject_has_tool_configs():
    """Test that pyproject.toml has tool configurations."""
    backend_path = Path(__file__).parent.parent / "backend"
    pyproject = backend_path / "pyproject.toml"

    if pyproject.exists():
        content = pyproject.read_text()
        assert "[tool.black]" in content, "pyproject.toml should have [tool.black] section"
        assert "[tool.mypy]" in content, "pyproject.toml should have [tool.mypy] section"
        assert "[tool.ruff]" in content, "pyproject.toml should have [tool.ruff] section"
