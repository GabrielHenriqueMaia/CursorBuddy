"""Test utilities and fixtures"""

import pytest
from unittest.mock import AsyncMock, MagicMock

# Fixtures will be added as tests are developed


@pytest.fixture
def mock_perception():
    """Mock perception module"""
    mock = AsyncMock()
    return mock


@pytest.fixture
def mock_context():
    """Mock context module"""
    mock = AsyncMock()
    return mock


@pytest.fixture
def mock_planning():
    """Mock planning module"""
    mock = AsyncMock()
    return mock


@pytest.fixture
def mock_execution():
    """Mock execution module"""
    mock = AsyncMock()
    return mock


@pytest.fixture
def mock_reflection():
    """Mock reflection module"""
    mock = AsyncMock()
    return mock


@pytest.fixture
def mock_memory():
    """Mock memory module"""
    mock = AsyncMock()
    return mock
