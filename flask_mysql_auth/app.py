from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User
import pymysql # Импортируем, чтобы Flask-SQLAlchemy мог его использовать
import os

app = Flask(__name__)

# --- Конфигурация базы данных ---
# Убедись, что все эти параметры соответствуют твоей настройке MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_mysql_password@localhost/flask_auth' # Замени 'your_mysql_password'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = 'your_super_secret_key_here' # Важно для сессий и flash-сообщений

# --- Создание таблиц (если они еще не существуют) ---
# Это нужно сделать один раз, чтобы база данных была готова
# Лучше делать это вне основного цикла приложения, например, через отдельный скрипт или команду Flask CLI
# Для простоты примера, можно раскомментировать и запустить один раз
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Пожалуйста, введите имя пользователя и пароль.', 'error')
            return redirect(url_for('login'))

        # Получаем пользователя из базы данных
        user = User.query.filter_by(user_name=username).first()

        if user and user.user_password == password: # Сравнение с паролем из БД (в реальном приложении - с хешем)
            session['username'] = username # Сохраняем имя пользователя в сессии
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None) # Удаляем имя пользователя из сессии
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Важно: перед первым запуском, если таблицы еще не созданы,
    # раскомментируйте блок db.create_all() выше и запустите скрипт один раз.
    # После создания таблиц закомментируйте его обратно.
    app.run(debug=True)
