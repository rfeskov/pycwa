import os
from flask import Flask
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

db_user     = os.environ.get('PYCWA_USER',      'pycwa')
db_password = os.environ.get('PYCWA_PASSWORD',  'pycwa')
db_host     = os.environ.get('PYCWA_DB_HOST',   'postgres')
db_database = os.environ.get('PYCWA_DATABASE',  'pycwa')

pgsql_pool = psycopg2.pool.ThreadedConnectionPool(1, 40, user=db_user,
                                                         password=db_password,
                                                         host=db_host,
                                                         port="5432",
                                                         database=db_database,
                                                         cursor_factory=RealDictCursor)

def create_app():
  app = Flask(__name__)

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)

  return app