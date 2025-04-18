"""
utils.py

Вспомогательные функции для проекта.
"""

import os
import json
import re

try:
    import yaml
except ImportError:
    yaml = None

def clean_review_text(text):
    """
    Удаляет все символы, кроме цифр, из строки с количеством отзывов.
    
    :param text: Исходная строка, например "1 459 отзывов".
    :return: Числовая строка, например "1459".
    """
    return re.sub(r'\D', '', text)

def load_config(config_path):
    """
    Загружает конфигурацию из файла формата JSON или YAML.

    :param config_path: Путь к конфигурационному файлу.
    :return: Словарь с настройками.
    :raises FileNotFoundError: Если файл не найден.
    :raises ImportError: Если пытаемся загрузить YAML, а пакет PyYAML не установлен.
    :raises ValueError: Если формат файла не поддерживается.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Конфигурационный файл не найден: {config_path}")

    ext = os.path.splitext(config_path)[1].lower()
    with open(config_path, "r", encoding="utf-8") as f:
        if ext == ".json":
            config = json.load(f)
        elif ext in [".yaml", ".yml"]:
            if yaml is None:
                raise ImportError("Для работы с YAML необходимо установить пакет PyYAML")
            config = yaml.safe_load(f)
        else:
            raise ValueError("Неподдерживаемый формат конфигурационного файла. Используйте JSON или YAML.")
    return config

def get_config_value(config, key_path, default=None):
    """
    Возвращает значение из конфигурации по ключу, заданному точечной нотацией.
    
    Например, для ключа "delays.startup" будет произведен поиск в словаре:
      config = { "delays": { "startup": 2.0 } }
    
    :param config: Словарь с конфигурацией.
    :param key_path: Строка с ключами, разделёнными точкой.
    :param default: Значение по умолчанию, если ключ не найден.
    :return: Значение параметра или default, если ключ не найден.
    """
    keys = key_path.split('.')
    val = config
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            return default
    return val
