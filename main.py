from app import app
from db_init import initialize_database


from routes import *



if __name__ == '__main__':
    # Инициализация базы данных перед запуском приложения
    initialize_database()

    # Запуск Flask-приложения
    app.run(debug=True)



