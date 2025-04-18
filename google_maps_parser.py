"""
google_maps_parser.py

Модуль, объединяющий функциональность для парсинга Google Maps.
Использует WebDriver для навигации, DataExtractor для получения данных 
и ExcelExporter для экспорта результатов в Excel.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from web_driver import WebDriverWrapper
from data_extractor import DataExtractor
from excel_exporter import ExcelExporter

class GoogleMapsParser:
    def __init__(self, config):
        self.config = config
        self.web_driver = WebDriverWrapper(config)
        self.data_extractor = DataExtractor(config)
        self.excel_exporter = ExcelExporter(config)
        self.base_url = self.config.get("urls", {}).get("base", "https://www.google.com/maps")
        self.startup_delay = self.config.get("delays", {}).get("startup", 2.0)
        self.search_input_selector = self.config.get("selectors", {}).get(
            "search_input", "input#searchboxinput"
        )
    
    def run(self):
        # 1) Инициализация драйвера и переход на страницу
        driver = self.web_driver.initialize_driver()
        driver.get(self.base_url)
        time.sleep(self.startup_delay)
        
        # 2) Закрываем баннер куки, если он есть
        try:
            consent_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Принять все')]")
                )
            )
            consent_btn.click()
            time.sleep(1)
            print("Баннер куки закрыт")
        except Exception:
            # Если кнопка не найдена — просто продолжаем
            print("Баннер куки не найден, продолжаем")

        # 3) Вводим поисковый запрос
        query = self.config.get("query")
        if query:
            search_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.search_input_selector))
            )
            search_input.click()
            time.sleep(0.5)
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.ENTER)
            time.sleep(self.config.get("delays", {}).get("search", 3.0))
        
        # 4) Извлечение данных и экспорт
        data = self.data_extractor.extract_data(driver)
        self.excel_exporter.export(data)
        
        # 5) Закрываем браузер
        driver.quit()
