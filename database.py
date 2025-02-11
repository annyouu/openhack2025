import mysql.connector
from mysql.connector import Error

# データベース接続設定
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': ''
}

# データベースに接続する関数
def connect():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("MySQLに接続しました")
            return conn
    except Error as e:
        print(f"MySQL接続エラー: {e}")
    return None

# データベースに食品データを挿入する関数
def insert_food(food_name):
    conn = connect()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        query = "INSERT INTO foods (name) VALUES (%s)"
        cursor.execute(query,(food_name, )) 
        conn.commit()
        print(f"{food_name}をデータベースに保存しました")
        return True
    except Error as e:
        print(f"データ保存エラー: {e}")
        return False
    finally:
        cursor.close()
        conn.close()



# 画像判別後にfoodsテーブルのデータを削除する関数
def clear_foods_table():
    conn = connect()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM foods"
        cursor.execute(query)
        conn.commit()
        print("前のデータを削除しました。")
    except Error as e:
        print(f"データ削除エラー: {e}")
    finally:
        cursor.close()
        conn.close()

