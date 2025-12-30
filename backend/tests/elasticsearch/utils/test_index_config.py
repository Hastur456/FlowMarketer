import pytest
from unittest.mock import MagicMock


@pytest.fixture
def logger():
    return MagicMock()
