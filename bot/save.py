from venv import logger
from db import add_workout_type_if_not_exists, save_workout_record

def save_training_data(chat_id, parsed_result):
    workout_data = []
    
    for item in parsed_result:
        if 'exercise' in item:
            workout_name = item['exercise']
            count = item.get('count', 0) 

            # Добавление типа тренировки, если его нет в базе
            result = add_workout_type_if_not_exists(workout_name)
            if result:
                logger.info(f"Тренировка '{workout_name}' добавлена в базу.")
            else:
                logger.info(f"Тренировка '{workout_name}' уже существует.")
            
            # Добавляем данные тренировки в список workout_data
            workout_data.append({
                "type": workout_name,
                "parameter": count
            })
    
    # Передаем все данные тренировки в save_workout_record
    save_workout_record(chat_id, workout_data)


