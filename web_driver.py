"""
web_driver.py

Модуль для работы с Selenium WebDriver.
Отвечает за инициализацию драйвера с использованием конфигурационных параметров.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class WebDriverWrapper:
    def __init__(self, config):
        self.config = config
        self.startup_delay = self.config.get("delays", {}).get("startup", 2.0)
        self.click_delay = self.config.get("delays", {}).get("click", 1.0)
        self.driver_path = self.config.get("driver_path")
        self.chrome_path = self.config.get("chrome_path")
    
    def initialize_driver(self):
        """
        Инициализирует Chrome WebDriver с указанными параметрами.
        """
        if not self.driver_path:
            raise ValueError(
                "Путь к chromedriver не указан. Укажите 'driver_path' в конфигурации или через аргументы."
            )
        
        service = Service(self.driver_path)
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # временно выключаем headless для отладки
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")    # для надежности
        options.add_argument("--no-sandbox")     # для Linux/CI
        if self.chrome_path:
            options.binary_location = self.chrome_path

        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(self.startup_delay)

        # Печать версий уже после инициализации драйвера
        print("Browser version:", driver.capabilities.get("browserVersion"))
        print("Chromedriver:", driver.capabilities.get("chrome", {}).get("chromedriverVersion"))

        return driver

    def click_element(self, element):
        element.click()
        time.sleep(self.click_delay)