import os
from backend.app import create_app

# Get environment
env = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(env)

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = app.config['DEBUG']

    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )
