import config

import psycopg2

con = psycopg2.connect(
        dbname="postgres",
        user=config.userDB,
        password=config.passDB,
        host=config.hostDB,
        port=config.portDB
    )

# Create a cursor object to interact with the database
cur = con.cursor()

async def create_table_users():
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL
    );"""
    )
    con.commit()

def user_exists(user_id, username):
    cur.execute("""SELECT * FROM users WHERE user_id = %s OR username = %s;""", (user_id, username))
    return cur.fetchone() is not None

async def add_user(user_id, username):
    try:
        if user_exists(user_id, username):
            print(f"Пользователь {username} уже зарегистрирован")
            return

        cur.execute("INSERT INTO users (user_id, username) VALUES (%s, %s)",
        (user_id, username))
        con.commit()
        print(f"Пользователь {username} успешно зарегистрирован")
    except Exception as e:
        print(f"Ошибка при регистрации пользователя {username}: {e}")



