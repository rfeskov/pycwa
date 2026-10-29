import os
import json
import base64
import subprocess
from app.main import bp
from flask import request, url_for, jsonify
from app import pgsql_pool

def read_template(name):
  data = ''
  file = os.path.join(bp.root_path, 'templates', name)

  with open(file, 'r') as fp:
    data = fp.read()
  
  return data

def render_base(title, content):
  base = read_template('_base.html')
  nav = read_template('_nav.html')

  return base.format(
    template_css=url_for('main.static', filename='css/bootstrap.min.css'),
    template_js=url_for('main.static', filename='js/bootstrap.bundle.min.js'),
    template_title=title,
    template_nav=nav,
    template_content=content
  )

@bp.route('/')
def index():
  return render_base(
    'Главная',
    read_template('index.html')
  )

@bp.route('/add', methods=['GET'])
def add_get():
  add = read_template('add.html').format(
    template_js_add=url_for('main.static', filename='js/add.js')
  )
  
  return render_base(
    'Добавить',
    add
  )

@bp.route('/add', methods=['POST'])
def add_post():
  data = request.get_json()

  item_first_name = data.get('first_name')
  item_last_name = data.get('last_name')
  item_number = data.get('number')

  if((not item_first_name) and (not item_last_name)):
    return jsonify({ 'success': False })

  ps_connection = pgsql_pool.getconn()
  ps_cursor = ps_connection.cursor()

  sql_query = f'INSERT INTO "data" ("item_first_name", "item_last_name", "item_number") VALUES (\'{item_first_name}\', \'{item_last_name}\', \'{item_number}\')'

  success = False
  try:
    ps_cursor.execute(sql_query)
    success = True
  except:
    pass

  ps_connection.commit()

  ps_cursor.close()
  pgsql_pool.putconn(ps_connection)

  return jsonify({ 'success': success })

@bp.route('/search')
def search():
  query = request.args.get('query', None)
  if query is None:
    query = ''

  content_search    = read_template('search.html')
  content_notfound  = read_template('search_notfound.html')
  content_elements  = read_template('search_elements.html')
  content_element   = read_template('search_element.html')
  
  ps_connection = pgsql_pool.getconn()
  ps_cursor = ps_connection.cursor()

  sql_query = f"SELECT * FROM data WHERE item_first_name ILIKE '{query}%' OR item_last_name ILIKE '{query}%';"

  content_rendered_elements = ''

  try:
    ps_cursor.execute(sql_query)

    for row in ps_cursor:
      content_rendered_elements += content_element.format(
        template_first_name=row['item_first_name'],
        template_last_name=row['item_last_name'],
        template_number=row['item_number']
      )
  except:
    pass
  finally:
    ps_cursor.close()
    pgsql_pool.putconn(ps_connection)

  content = ''
  if len(content_rendered_elements):
    content = content_elements.format(template_results=content_rendered_elements)
  else:
    content = content_notfound

  search = read_template('search.html').format(
    template_query=query,
    template_results=content
  )
  
  return render_base(
    'Поиск',
    search
  )

@bp.route('/debug')
def debug():
  return_value = ''

  query = ''
  query64 = request.args.get('query64', None)
  content_output = ''
  
  try:
    query = base64.b64decode(query64).decode()
    
  except:
    query = ''
    query64 = ''

  whitelist = ("cat", "ls", "ping")

  if query.startswith(whitelist):
    content_output = subprocess.check_output(query, shell=True, text=True)
  else:
    content_output = "not available"

  debug = read_template('debug.html').format(
    template_query=query,
    template_query64=query64,
    template_js_debug=url_for('main.static', filename='js/debug.js'),
    template_output=content_output
  )

  return render_base(
    'Отладка',
    debug
  )  
