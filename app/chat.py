from flask import flash, redirect, render_template, session, url_for
from flask_socketio import SocketIO, send

from .views import app

socketio = SocketIO(app)


@app.route("/chat/")
def chat():
    if "username" not in session:
        flash("Вы должны быть залогинены для общения в чате.", "danger")
        return redirect(url_for("login"))
    return render_template("chat.html")


# Обработчик WebSocket-сообщений
@socketio.on("connect")
def handle_connect():
    if "username" not in session:
        send("Вы должны быть залогинены для общения в чате.", broadcast=False)
        return False
    username = session["username"]
    send(f"{username} has entered the chat!", broadcast=True)


@socketio.on("message")
def handle_message(msg):
    if "username" not in session:
        send("Вы должны быть залогинены для общения в чате.", broadcast=False)
        return
    user = session["username"]
    send(f"{user}: {msg}", broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    if "username" in session:
        username = session["username"]
        send(f"{username} has left the chat.", broadcast=True)
