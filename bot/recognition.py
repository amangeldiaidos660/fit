import os
import re
import json
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

def word_to_number_ru(word):
    number_map = {
        "ноль": 0, "один": 1, "два": 2, "три": 3, "четыре": 4,
        "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9,
        "десять": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13,
        "четырнадцать": 14, "пятнадцать": 15, "шестнадцать": 16,
        "семнадцать": 17, "восемнадцать": 18, "девятнадцать": 19,
        "двадцать": 20, "тридцать": 30, "сорок": 40, "пятьдесят": 50,
        "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80, "девяносто": 90,
        "сто": 100
    }
    return number_map.get(word.lower(), None)

@lru_cache(maxsize=1)
def load_keywords(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["keywords"]

def prepare_keyword_patterns(keywords):
    patterns = {}
    for exercise, variations in keywords.items():
        patterns[exercise] = re.compile(r"|".join(map(re.escape, variations)), re.IGNORECASE)
    return patterns

def extract_count(user_text):
    number_pattern = r"\b(?:\d+|[а-яё]+)\b"
    matches = re.findall(number_pattern, user_text, re.IGNORECASE)

    for match in matches:
        if match.isdigit():
            return int(match)
        count = word_to_number_ru(match)
        if count is not None:
            return count
    
    return None

def analyze_exercise(user_text, keyword_patterns):
    detected_exercises = []
    for exercise, pattern in keyword_patterns.items():
        if pattern.search(user_text):
            count = extract_count(user_text)
            detected_exercises.append({"exercise": exercise, "count": count})
    
    if detected_exercises:
        return detected_exercises
    return [{"message": "Не удалось определить упражнение из текста."}]

def analyze_text(text):
    current_dir = os.path.dirname(__file__)
    words_file_path = os.path.join(current_dir, "words.json")
    keywords = load_keywords(words_file_path)
    keyword_patterns = prepare_keyword_patterns(keywords)
    results = analyze_exercise(text, keyword_patterns)
    return json.dumps(results, ensure_ascii=False, indent=4)


