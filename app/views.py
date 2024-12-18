import os
from datetime import datetime

from cryptography.fernet import Fernet
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    abort,
)
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import (
    LoginForm,
    PrivateMessageForm,
    UserForm,
    CommentForm,
    CSRFForm,
)
from .models import (
    Chats,
    Plants,
    PrivateMessage,
    Users,
    UsersPlants,
    Comments,
    db,
)
from .utils import decrypt_message, encrypt_message, login_checker

key = Fernet.generate_key()

key = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(key)

app = Flask(__name__)


@app.route("/")
def main():
    per_page = 15
    page = request.args.get("page", 1, type=int)

    plants = Plants.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template("index.html", plants=plants)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/cart/<int:id>", methods=["GET", "POST"])
def cart(id):
    plant = Plants.query.get_or_404(id)
    is_collect = False
    form = CommentForm()
    if session.get("login") is True:
        user_id = session.get("id")
        collect = UsersPlants.query.filter(
            UsersPlants.user_id == user_id, UsersPlants.plant_id == id
        ).first()
        if collect is not None:
            is_collect = True

        if request.method == "POST":
            now = datetime.now()
            now_without_seconds = now.replace(microsecond=0)
            text = form.text.data
            plant_id = id
            new_comment = Comments(
                user_id=user_id,
                plant_id=plant_id,
                text=text,
                timestamp=now_without_seconds,
            )
            db.session.add(new_comment)
            db.session.commit()
            flash("Комментарий добавлен!", "success")
            return redirect(url_for("cart", id=id))

    return render_template(
        "cart.html", plant=plant, is_collect=is_collect, form=form
    )


@app.route("/collect/<int:id>")
def collect(id):
    user_id = session["id"]
    new_collect = UsersPlants(user_id=user_id, plant_id=id)
    db.session.add(new_collect)
    db.session.commit()
    flash("Успешно добавлено!", "success")
    return redirect(url_for("cart", id=id))


@app.route("/discollect/<int:id>")
def discollect(id):
    user_id = session.get("id")
    collect = UsersPlants.query.filter(
        UsersPlants.user_id == user_id, UsersPlants.plant_id == id
    ).first()
    db.session.delete(collect)
    db.session.commit()
    flash("Успешно удалено!", "danger")
    return redirect(url_for("cart", id=id))


@app.route("/comment/<int:id>", methods=["GET", "POST"])
def comment(id):
    form = CommentForm()
    comment = Comments.query.get_or_404(id)
    if request.method == "POST":
        if (
            comment.user_id == session.get("id")
            or session.get("is_admin") is True
        ):
            text = form.text.data
            comment.text = text
            db.session.commit()
            return redirect(url_for("comment", id=id))
        else:
            abort(403)
    return render_template(
        "comment.html", form=form, comment=comment, route="get"
    )


@app.route("/delete_comment/<int:id>", methods=["GET", "POST"])
def delete_comment(id):
    comment = Comments.query.get_or_404(id)
    form = CSRFForm()
    if comment.user_id == session.get("id") or session.get("is_admin") is True:
        if request.method == "POST":
            print(213)
            cart = comment.plant_id
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for("cart", id=cart))
        return render_template(
            "comment.html", comment=comment, form=form, route="delete"
        )
    else:
        abort(403)


@app.route("/register/", methods=["GET", "POST"])
def register():
    form = UserForm()
    if request.method == "POST":
        if form.password.data != form.confirmPassword.data:
            flash("Пароли не совпадают!", "danger")
            return render_template("register.html", form=form)
        hash_password = generate_password_hash(form.password.data)
        new_user = Users(
            username=form.username.data,
            password=hash_password,
            email=form.email.data,
        )
        db.session.add(new_user)
        db.session.commit()
        flash(
            "Вы успешно зарегистрировались и теперь можете войти со своим логином и паролем!",
            "success",
        )
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        username = form.username.data
        user = Users.query.filter_by(username=username).first_or_404()
        if check_password_hash(user.password, form.password.data):
            session["login"] = True
            session["username"] = user.username
            session["id"] = user.id
            session["is_admin"] = user.is_admin
            flash("Вы успешно вошли в систему!", "success")
        else:
            flash("Неверный логин или пароль!", "danger")
            return render_template("login.html", form=form)
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout/")
def logout():
    session.clear()
    flash("Вы вышли из системы!", "success")
    return redirect("/")


@app.route("/profile/")
def profile():
    login_checker()
    username = session["username"]
    user = Users.query.filter_by(username=username).first_or_404()
    return render_template("profile.html", user=user, route=request.endpoint)


@app.route("/user/<int:id>")
def user(id):
    user = Users.query.get_or_404(id)
    return render_template("profile.html", user=user, route=request.endpoint)


@app.route("/users/")
def users():
    users = Users.query.all()
    return render_template("users.html", users=users)


@app.route("/private_messages/<int:id>", methods=["GET", "POST"])
def private_messages(id):
    form = PrivateMessageForm()
    user_id = session["id"]
    users = "|".join(sorted((str(id), str(user_id))))

    chat = Chats.query.filter_by(users=users).first()
    if chat is None:
        new_chat = Chats(users=users)
        db.session.add(new_chat)
        db.session.commit()
        chat = Chats.query.filter_by(users=users).first()

    if request.method == "POST":

        now = datetime.now()
        now_without_seconds = now.replace(microsecond=0)
        encrypted_message = encrypt_message(form.text.data, cipher_suite)

        new_pm = PrivateMessage(
            chat_id=chat.id,
            sender_id=user_id,
            recipient_id=id,
            message=encrypted_message,
            timestamp=now_without_seconds,
        )
        db.session.add(new_pm)
        db.session.commit()
        return redirect(url_for("private_messages", id=id))

    messages = (
        PrivateMessage.query.filter(PrivateMessage.chat_id == chat.id)
        .order_by(PrivateMessage.timestamp.desc())
        .all()
    )
    unreaded_messages = (
        PrivateMessage.query.filter(
            PrivateMessage.chat_id == chat.id,
            PrivateMessage.recipient_id == user_id,
            PrivateMessage.is_readed == False,
        )
        .order_by(PrivateMessage.timestamp.desc())
        .all()
    )
    for message in unreaded_messages:
        message.is_readed = True
        db.session.commit()

    for message in messages:
        message.message = decrypt_message(message.message, cipher_suite)

    return render_template(
        "private_messages.html", messages=messages, form=form, id=id
    )


@app.route("/private_chats/")
def private_chats():
    login_checker()
    user_id = session["id"]

    chats = (
        Chats.query.with_entities(Chats.id)
        .filter(
            (Chats.users.like(f"{user_id}|%"))
            | (Chats.users.like(f"%|{user_id}"))
        )
        .all()
    )
    chat_ids = [chat[0] for chat in chats]

    chats_senders = (
        PrivateMessage.query.filter((PrivateMessage.chat_id.in_(chat_ids)))
        .group_by(PrivateMessage.chat_id)  # Группировка по sender_id
        .order_by(
            func.max(PrivateMessage.timestamp).desc()
        )  # Сортировка по времени последнего сообщения
        .all()
    )

    return render_template("private_chats.html", chats=chats_senders)


@app.errorhandler(404)
def render_not_found(error):
    return render_template("error.html", error="Страница не найдена")


@app.errorhandler(403)
def render_forbidden(error):
    return render_template(
        "error.html", error="У вас нет прав для просмотра этой страницы"
    )


@app.errorhandler(500)
def render_server_error(error):
    return render_template(
        "error.html", error="У нас случилась проблема, но скоро мы её решим!"
    )


@app.before_request
def load_user():
    if "id" in session:
        user_id = session["id"]
        new_messages = PrivateMessage.query.filter(
            PrivateMessage.recipient_id == user_id,
            PrivateMessage.is_readed == False,
        ).count()
        session["new_messages"] = new_messages
