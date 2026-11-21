from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Важно для flash-сообщений

# Захардкоженные пользователи для примера
# В реальном приложении данные хранятся в базе данных
USERS = {
    "admin": "password",
    "user": "12345"
}

@app.route('/')
def index():
    # Если пользователя нет в сессии (или он вышел), перенаправляем на страницу входа
    if 'username' not in request.cookies: # Проверяем cookie, а не сессию для простоты
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверка на пустые поля (клиентская валидация уже есть в HTML, но серверная тоже нужна)
        if not username or not password:
            flash('Пожалуйста, введите имя пользователя и пароль.', 'error')
            return redirect(url_for('login'))

        # Проверка учетных данных
        if username in USERS and USERS[username] == password:
            # Успешная авторизация: устанавливаем cookie и перенаправляем на index
            # В реальном приложении здесь лучше использовать сессии
            response = redirect(url_for('index'))
            response.set_cookie('username', username) # Устанавливаем cookie с именем пользователя
            return response
        else:
            # Неверные учетные данные
            flash('Неверное имя пользователя или пароль.', 'error')
            return redirect(url_for('login'))

    # GET запрос: просто показываем форму входа
    # flash-сообщения будут отображены в шаблоне login.html
    return render_template('login.html', error=None) # error здесь не используется, т.к. flash лучше

@app.route('/logout')
def logout():
    # Удаляем cookie пользователя при выходе
    response = redirect(url_for('login'))
    response.delete_cookie('username')
    return response

if __name__ == '__main__':
    app.run(debug=True)
