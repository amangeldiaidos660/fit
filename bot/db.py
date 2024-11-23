from datetime import datetime
import json
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

def add_workout_type_if_not_exists(workout_name):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM tracker_workouttype WHERE name = %s",
                (workout_name,)
            )
            result = cursor.fetchone()

            if result:
                return False
            
            cursor.execute(
                "INSERT INTO tracker_workouttype (name) VALUES (%s)",
                (workout_name,)
            )
            connection.commit()
            return True  
    except Exception as e:
        return False, f"Ошибка работы с базой: {e}"
    finally:
        connection.close()

def save_workout_record(chat_id, workout_data):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM tracker_user WHERE chat_id = %s",
                (chat_id,)
            )
            user_id_result = cursor.fetchone()

            if not user_id_result:
                return False

            user_id = user_id_result[0]

            current_date = datetime.now().strftime("%Y-%m-%d")

            cursor.execute(
                "SELECT workout_data FROM tracker_record WHERE user_id = %s AND workout_date = %s",
                (user_id, current_date)
            )
            existing_record = cursor.fetchone()

            if existing_record:
                existing_data = existing_record[0]

                for new_workout in workout_data:
                    workout_name = new_workout['type']
                    count = new_workout['parameter']
                    
                    workout_found = False
                    for existing_workout in existing_data:
                        if existing_workout['type'] == workout_name:
                            existing_workout['parameter'] += count
                            workout_found = True
                            break
                    
                    if not workout_found:
                        existing_data.append(new_workout)

                if isinstance(existing_data, list):
                    serialized_data = json.dumps(existing_data)
                else:
                    return False

                cursor.execute(
                    "UPDATE tracker_record SET workout_data = %s WHERE user_id = %s AND workout_date = %s",
                    (serialized_data, user_id, current_date)
                )
            else:
                if isinstance(workout_data, list):
                    serialized_data = json.dumps(workout_data)
                else:
                    return False

                cursor.execute(
                    "INSERT INTO tracker_record (user_id, workout_data, workout_date) VALUES (%s, %s, %s)",
                    (user_id, serialized_data, current_date)
                )

            connection.commit()
            return True
    except Exception as e:
        return False
    finally:
        connection.close()
