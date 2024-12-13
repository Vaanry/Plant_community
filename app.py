from threading import Thread

from flask_migrate import Migrate

from .admin import admin
from .chat import socketio
from .models import db
from .settings import Config
from .views import app

app.config.from_object(Config)

app.debug = True
app.jinja_env.cache = None
db.init_app(app)

migrate = Migrate(app, db)


def run_flask():
    app.run(debug=True, threaded=True)


def run_socketio():
    socketio.run(app, debug=True, use_reloader=False)


if __name__ == "__main__":
    # Запуск Flask и SocketIO в отдельных потоках
    flask_thread = Thread(target=run_flask)
    socketio_thread = Thread(target=run_socketio)

    flask_thread.start()
    socketio_thread.start()
