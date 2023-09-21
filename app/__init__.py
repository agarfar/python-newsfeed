from flask import Flask
from app.routes import home, dashboard
from app.db import init_db
from app.utils import filters

def create_app(test_config=None):
  # set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )
  app.jinja_env.filters['format_url'] = filters.format_url
  app.jinja_env.filters['format_date'] = filters.format_date
  app.jinja_env.filters['format_plural'] = filters.format_plural
  # To use your custom filter functions, you need to register them with the Jinja template environment. 

  @app.route('/hello')
  def hello():
    return 'hello world'
  
  app.register_blueprint(home)
  app.register_blueprint(dashboard)

  init_db(app)
  # Thanks to these updates, we no longer have to worry about connections remaining open and potentially locking up the server. added 'app' to init_db() call

  return app