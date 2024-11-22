from config import connect_to_db

def check_user_in_db(email, hashed_password, chat_id):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT password FROM tracker_user WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
            if result and result[0] == hashed_password:
                cursor.execute(
                    "UPDATE tracker_user SET chat_id = %s WHERE email = %s",
                    (chat_id, email)
                )
                connection.commit()
                return True, "Авторизация успешна."
            return False, "Неверный email или пароль."
    except Exception as e:
        return False, f"Ошибка работы с базой: {e}"
    finally:
        connection.close()
