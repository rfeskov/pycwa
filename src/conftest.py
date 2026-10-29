import pytest
from bs4 import BeautifulSoup
from app import create_app

@pytest.fixture
def client():
  app = create_app()

  yield app.test_client()

@pytest.fixture
def get_soup(client):
  def _get(path, **kwargs):
    response = client.get(path, **kwargs)
    soup = BeautifulSoup(response.data, "html.parser")
    return response, soup
  return _get