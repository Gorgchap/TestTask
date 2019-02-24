# TestTask
Especially for Advance (https://advance.careers)

Before starting you must install Sqlite3 and Anaconda3 on your local PC. Then you should create new conda venv testtask (Python version: 3.7.2).
conda activate testtask
set FLASK_APP=runserver.py
flask db init
flask db migrate -m "db"
flask db upgrade
flask run
Personally I created two users: robot5002@mail.ru (password: 1) and mattheafy027@gmail.com (password: 1). Both of these users bought some goods.