"""
data_extractor.py

Модуль для извлечения данных о заведениях из карточек результатов Google Maps.
Использует Selenium для навигации по элементам и получения деталей заведения.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils import clean_review_text

class DataExtractor:
    def __init__(self, config):
        self.config = config
        self.max_results = self.config.get("max_results", 5)
        # Селектор карточки результатов. Если это просто имя класса, ищем по CLASS_NAME.
        self.card_selector = self.config.get("selectors", {}).get("result_card", "hfpxzc")
        # Селекторы для деталей заведения
        self.detail_name_selector = self.config.get("selectors", {}).get("detail_name", "DUwDvf")
        self.detail_rating_xpath = self.config.get("selectors", {}).get("detail_rating", '//div[contains(@class,"F7nice")]//span[@aria-hidden="true"]')
        self.detail_address_xpath = self.config.get("selectors", {}).get("detail_address", '//div[contains(@class, "Io6YTe") and contains(@class, "kR99db")]')
        self.detail_reviews_xpath_options = [
            self.config.get("selectors", {}).get("detail_reviews_option1", '//div[contains(@class,"F7nice")]//span[contains(@aria-label, "отзыва")]'),
            self.config.get("selectors", {}).get("detail_reviews_option2", '//button[contains(@aria-label,"отзывы")]')
        ]

    def extract_data(self, driver):
        results = []
        
        # Если селектор начинается с '.' или '#' – используем CSS-селектор, иначе CLASS_NAME
        if self.card_selector.startswith('.') or self.card_selector.startswith('#'):
            places = driver.find_elements(By.CSS_SELECTOR, self.card_selector)
        else:
            places = driver.find_elements(By.CLASS_NAME, self.card_selector)
        
        print(f"Найдено карточек: {len(places)}")
        
        places = places[:self.max_results]

        for index, place in enumerate(places, 1):
            try:
                # Клик на карточку для открытия деталей заведения
                ActionChains(driver).move_to_element(place).click().perform()
                # Ожидание загрузки деталей (ожидаем появление элемента с названием)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, self.detail_name_selector))
                )
                time.sleep(3)  # Дополнительная задержка для загрузки деталей

                # Извлечение названия заведения
                name_elem = driver.find_element(By.CLASS_NAME, self.detail_name_selector)
                name = name_elem.text.strip()

                # Извлечение рейтинга заведения
                try:
                    rating_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.detail_rating_xpath))
                    )
                    rating = rating_element.text.strip()
                except Exception:
                    rating = "No rating"

                # Извлечение адреса заведения
                try:
                    address_element = driver.find_element(By.XPATH, self.detail_address_xpath)
                    address = address_element.text.strip()
                except Exception:
                    address = None

                # Извлечение количества отзывов
                reviews = "0"
                for xpath_option in self.detail_reviews_xpath_options:
                    try:
                        reviews_element = driver.find_element(By.XPATH, xpath_option)
                        reviews_label = reviews_element.get_attribute("aria-label")
                        reviews = clean_review_text(reviews_label)
                        if reviews == "":
                            reviews = "0"
                        break
                    except Exception:
                        continue

                results.append({
                    "Name": name,
                    "Rating": rating,
                    "Address": address,
                    "Review Count": reviews
                })
                print(f"[{index}] ✅ {name} — Rating: {rating}, Address: {address or 'None'}, Reviews: {reviews}")
            except Exception as e:
                print(f"[{index}] ⚠️ Ошибка: {e}")
                continue

        return results
