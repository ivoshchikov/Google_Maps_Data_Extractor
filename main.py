#!/usr/bin/env python3
"""
main.py

Основной файл для запуска проекта Google Maps Data Extractor.
Обрабатывает аргументы командной строки, загружает конфигурацию и 
создаёт объект GoogleMapsParser, который выполняет парсинг данных и сохраняет их в Excel.
"""

import argparse
from utils import load_config
from google_maps_parser import GoogleMapsParser

def main():
    parser = argparse.ArgumentParser(description="Google Maps Data Extractor")
    parser.add_argument("--config", default="config.json",
                        help="Путь к файлу конфигурации (JSON или YAML)")
    parser.add_argument("--query", type=str, required=True,
                        help="Поисковый запрос для Google Maps (например, 'coffee Larnaca')")
    parser.add_argument("--max_results", type=int, default=5,
                        help="Максимальное количество результатов (по умолчанию 5)")
    parser.add_argument("--driver_path", type=str, required=True,
                        help="Путь к исполняемому файлу chromedriver")
    parser.add_argument("--chrome_path", type=str, default="",
                        help="Путь к исполняемому файлу Google Chrome (если отличается от стандартного)")
    parser.add_argument("--output", type=str, default="results.xlsx",
                        help="Имя выходного Excel-файла (по умолчанию 'results.xlsx')")
    args = parser.parse_args()

    # Загрузка конфигурации из файла
    config = load_config(args.config)

    # Переопределяем (override) настройки значениями из командной строки
    config["query"] = args.query
    config["max_results"] = args.max_results
    config["driver_path"] = args.driver_path
    config["chrome_path"] = args.chrome_path
    config.setdefault("export", {})["filename"] = args.output

    # Создаем и запускаем парсер Google Maps с переданной конфигурацией
    parser_instance = GoogleMapsParser(config)
    parser_instance.run()

if __name__ == "__main__":
    main()
