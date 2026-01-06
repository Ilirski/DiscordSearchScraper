"""Pytest configuration and fixtures."""


import pytest


@pytest.fixture
def tmp_path(tmp_path_factory):
    """Fixture providing a temporary directory path."""
    return tmp_path_factory.mktemp("test_scraper")


@pytest.fixture
def temp_output_file(tmp_path):
    """Fixture providing a temporary output file path."""
    return str(tmp_path / "test_output.jsonl")
