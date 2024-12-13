import re
from flask import Flask, flash, render_template, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Задайте URI для вашей БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False, nullable=False)

# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')


# Маршрут для обработки формы
@app.route('/submit', methods=['POST'])
def submit_form():
    # Получаем данные из формы
    email = request.form['textInput']
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
          # Проверка с помощью регулярного выражения
        if ".ru" in email: # Добавляем проверку на .ru, если это необходимо
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
        else:
            flash('Пожалуйста, укажите email адрес с доменом .ru')
            return redirect(url_for('your_form_route')) # Перенаправить на форму
    else:
        flash('Пожалуйста, укажите корректный email адрес')
        return redirect(url_for('your_form_route')) # Перенаправить на форму
        
    # Перенаправляем на главную страницу или другую страницу
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
