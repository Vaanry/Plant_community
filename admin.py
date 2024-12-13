from flask import abort, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import Plants, Users, db
from .views import app

app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(app, name="Admin", template_mode="bootstrap3")


class SecureBaseModelView(ModelView):
    def is_accessible(self):
        # Проверяем, есть ли пользователь в сессии
        user_id = session.get("id")
        if not user_id:
            return False

        # Получаем пользователя из базы
        user = Users.query.get(user_id)
        return user.is_admin if user else False

    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class UsersAdminView(SecureBaseModelView):
    form_excluded_columns = ["users_plants"]  # Исключаем отношение из форм
    column_exclude_list = [
        "users_plants",
        "password",
    ]  # Исключаем отношение из колонок
    can_delete = False
    page_size = 50


class PlantsAdminView(SecureBaseModelView):
    form_excluded_columns = ["plants_users"]
    column_exclude_list = ["plants_users"]
    can_view_details = True


admin.add_view(UsersAdminView(Users, db.session))
admin.add_view(PlantsAdminView(Plants, db.session))
