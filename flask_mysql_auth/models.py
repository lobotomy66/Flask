from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users' # Важно, чтобы совпадало с именем таблицы в БД

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False) # В реальном приложении здесь должен быть хеш пароля

    def __repr__(self):
        return f'<User {self.user_name}>'
