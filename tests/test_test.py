import os
from dotenv import load_dotenv

# Загружаем .env файл перед инициализацией приложения
load_dotenv()

import pytest
from app import app, db  # Замените на ваш модуль приложения
from app.models import Plants  # Импортируйте свои модели


@pytest.fixture
def client():
    # Включаем тестирование
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI"
    )

    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def populate_data(client):
    plant1 = Plants(
        name="Ficus", species="Ficus elastica", description="A rubber plant."
    )
    plant2 = Plants(
        name="Monstera",
        species="Monstera deliciosa",
        description="A Swiss cheese plant.",
    )

    db.session.add(plant1)
    db.session.add(plant2)
    db.session.commit()

    yield  # Тесты выполняются тут

    # Удаляем тестовые данные после выполнения тестов
    db.session.query(Plants).filter(
        Plants.name.in_(["Ficus", "Monstera"])
    ).delete()
    db.session.commit()


def test_main_route(client, populate_data):
    # Проверяем, что на главной странице отображаются данные
    response = client.get("/")
    assert response.status_code == 200
    assert b"Ficus" in response.data
    assert b"Monstera" in response.data


def test_template_rendering(client, populate_data):
    # Проверяем рендеринг шаблона
    response = client.get("/")
    assert "Каталог растений" in response.data.decode("utf-8")


def test_invalid_page(client):
    # Проверяем обработку неправильного параметра страницы
    response = client.get("/cart/invalid")
    assert response.status_code == 200
    assert "Страница не найдена" in response.data.decode("utf-8")
