from app import create_app

def test_index_page(get_soup):
  _, soup = get_soup("/")
  form = soup.find("form")
  assert form is not None
  assert form.find("input", {"name": "query"})
  assert "Главная" in soup.title.string

def test_add_get(get_soup):
  _, soup = get_soup("/add")
  form = soup.find("form")
  assert form is not None
  assert form.find("input", {"name": "first_name"})
  assert form.find("input", {"name": "last_name"})
  assert form.find("input", {"name": "number"})
  assert "Добавить" in soup.title.string

def test_add_post(client):
  response = client.post(
      "/add",
      json={
        "first_name": 'test1',
        "last_name": 'test2',
        "number": 123
      }
  )

  assert response.status_code == 200
  data = response.get_json()
  assert data["success"]