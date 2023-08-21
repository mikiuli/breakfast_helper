from getpass import getpass
from mysql.connector import connect, Error
from parser_1 import get_a_recipe


def connect_with_server():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: ")
        ) as connection:
            print(connection)
    except Error as e:
        print(e)

def create_database():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: ")
        ) as connection:
            create_db_query = "CREATE DATABASE breakfast_helper"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)

def show_databases():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: ")
        ) as connection:
            show_db_query = "SHOW DATABASES"
            with connection.cursor() as cursor:
                cursor.execute(show_db_query)
                for db in cursor:
                    print(db)
    except Error as e:
        print(e)

def connect_with_database():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: "),
            database="breakfast_helper"
        ) as connection:
            print(connection)
    except Error as e:
        print(e)

def create_breakfast_table():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: "),
            database="breakfast_helper"
        ) as connection:
            create_breakfast_table_query = """
CREATE TABLE breakfast(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    list_of_ingredients VARCHAR(350),
    protein INT,
    fats INT,
    carbohydrates INT,
    calories INT,
    portions INT,
    time_for_cooking VARCHAR(15),
    picture_url VARCHAR(100),
    dish_url VARCHAR(100)
)"""
            with connection.cursor() as cursor:
                cursor.execute(create_breakfast_table_query)
                connection.commit()
    except Error as e:
        print(e)

def drop_breakfast_table():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: "),
            database="breakfast_helper"
        ) as connection:
            drop_breakfast_table_query = """
DROP TABLE breakfast
"""
            with connection.cursor() as cursor:
                cursor.execute(drop_breakfast_table_query)
    except Error as e:
        print(e)

def insert_into_table_breakfast(func_generator):
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass("Пароль: "),
            database="breakfast_helper"
        ) as connection:
            insert_into_breakfast_query = """
INSERT INTO breakfast (name,
    list_of_ingredients,
    protein,
    fats,
    carbohydrates,
    calories,
    portions,
    time_for_cooking,
    picture_url,
    dish_url)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            breakfast_recipes = [recipe for recipe in func_generator()]
            with connection.cursor() as cursor:
                cursor.executemany(insert_into_breakfast_query, breakfast_recipes)
                connection.commit()
    except Error as e:
        print(e)

def show_breakfast_table():
    try:
        with connect(
            host="localhost",
            user=input("Имя пользователя: "),
            password=getpass(),
            database="breakfast_helper"
        ) as connection:
            select_all_from_breakfast_table = """
SELECT * FROM breakfast"""
            with connection.cursor() as cursor:
                cursor.execute(select_all_from_breakfast_table)
                result = cursor.fetchall()
                for row in result:
                    print(row)
    except Error as e:
        print(e)

# create_breakfast_table()
# insert_into_table_breakfast(get_a_recipe)
# show_breakfast_table()