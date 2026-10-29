# Разработка
- убедиться, что файл `docker-compose.override.yml` на месте
- `docker compose up`

# Тесты
```
pip3 install -r src/requirements.txt

docker compose run -d --rm -p 5432:5432 postgres

PYCWA_DB_HOST=localhost PYCWA_PASSWORD=example pytest
```

Остановка тестов после этого

```
docker compose kill postgres

docker volume rm pycwa_db
```

# Прод
- убедиться, что файл docker-compose.override.yml- переименован (есть на конце -)
- `docker compose up`