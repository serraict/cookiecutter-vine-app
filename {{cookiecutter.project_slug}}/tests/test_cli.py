"""Tests for CLI commands."""

from pytest import MonkeyPatch
from typer.testing import CliRunner
from {{cookiecutter.project_slug}}.__cli__ import app
from {{cookiecutter.project_slug}}.products.models import Product

runner = CliRunner()


def test_version():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "version" in result.stdout


def test_products_command(monkeypatch: MonkeyPatch):
    """Test products list command."""
    class MockProductRepository:
        def get_all(self):
            return [
                Product(
                    id=1,
                    name="Test Product 1",
                    product_group_id=100,
                    product_group_name="Test Group A",
                ),
                Product(
                    id=2,
                    name="Test Product 2",
                    product_group_id=200,
                    product_group_name="Test Group B",
                ),
            ]

    monkeypatch.setattr(
        "{{cookiecutter.project_slug}}.__cli__.ProductRepository",
        lambda: MockProductRepository(),
    )

    result = runner.invoke(app, ["products"])
    assert result.exit_code == 0
    assert "Products" in result.stdout
    assert "Test Product 1" in result.stdout
    assert "Test Group A" in result.stdout
    assert "Test Product 2" in result.stdout
    assert "Test Group B" in result.stdout
