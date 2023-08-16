<div align=center>
    <h1>Основною ідеєю проєкту є спрощення керування чатом.</h1>
    <h1><p>Нижче можна ознайомитися з функціоналом боту:</p></h1>
</div>

    Список команд:

    👥 /start - додає користувача до БД.

    👥 /stat - надає статистику користувача.

    👥 /info - надає інформація про користувача.

    👥 /help - список команд.

    👥 /settings - налаштування видалення посилань.

    👮🏻‍♂️ /ban - дозволяє заблокувати користувача в групі, не даючи йому можливості приєднатися знову використовуючи посилання групи.

    👮🏻‍♂️ /unban - дозволяє видалити користувача з чорного списку групи, надавши можливість знову приєднатися за посиланням групи.

    👮🏻‍♂️ /kick - блокує користувача з групи, даючи можливість знову приєднатися за посиланням групи.

    👮🏻‍♂️ /mute - переводить користувача в режим тільки для читання. Він може читати, але не може надсилати повідомлення.

    👮🏻‍♂️ /unmute - повертає користувачу можливість відправляти повідомлення.

    👥 /rules - дозволяє дізнатися правила групи (для всіх). Дозволяє додати та оновити правила групи (Тільки для адміністраторів).

    👮🏻‍♂️ /rmrules - видаляє правила групи.

Деякі команди будуть доступні лише для адміністраторів, а я деякі для всіх (👮🏻‍♂️ - Доступно тільки для адміністраторів. 👥 - Доступно всім).

А також бот буде рахувати повідомлення користувачів, видаляти повідомлення, змінюватиме можливості користувачів у чаті.

<h1>Лінк на лендінг: <a href='https://nikita88575.github.io/my_projects.html'>Лендінг</a></h1>
<h1>Лінк на телеграм бота: <a href='https://t.me/chat_auxiliary_bot'>Бот</a></h1>
<h1>Лінк на Backend телеграм бота: <a href='https://github.com/Nikita88575/Telegram_Bot_with_Flask/tree/main/telegram_bot'>Backend телеграм бота</a></h1>
<h1>Запуск телеграм бота:</h1> 

## <p>Linux:</p>

1) Створюємо роль з паролем для бд:

```
sudo su postgres
createuser username -P --interactive
```
Робимо нову роль суперкористувачем.

2) Створюємо БД та виходимо з psql:

```
psql
CREATE DATABASE database_name;
\q
```
3) Переходимо директорію data в та створюємо файл .env на основі .env.example

2) Створюємо virtualenv:
```
python3 -m venv .venv
```
3) Активуємо virtualenv:
```
source .venv/bin/activate
```
4) Встановлюємо необхідні модулі:
```
pip3 install -r requirements.txt
```
5) Запускаємо бота:
```
.venv/bin/python3 app.py
```

<h1>Доповненням до бота є flask aplication задача якого полягає у перегладі даних в БД</h1>
<h1>Запуск додатку:</h1>

1) Переходимо директорію flask

2) Переходимо директорію data в та створюємо файл .env на основі .env.example

3) Створюємо virtualenv:
```
python3 -m venv .venv
```
4) Активуємо virtualenv:
```
source .venv/bin/activate
```
5) Встановлюємо необхідні модулі:
```
pip3 install -r requirements.txt
```
6) Запускаємо додаток:
```
.venv/bin/python3 app.py
```
