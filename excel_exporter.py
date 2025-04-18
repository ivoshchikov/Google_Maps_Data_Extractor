"""
excel_exporter.py

Модуль для экспорта данных в Excel-формат.
"""

import pandas as pd

class ExcelExporter:
    def __init__(self, config):
        self.config = config
        self.filename = self.config.get("export", {}).get("filename", "results.xlsx")
    
    def export(self, data):
        # Если данные представляют собой список словарей, преобразуем их в DataFrame,
        # иначе считаем их одномерным списком.
        if data and isinstance(data[0], dict):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(data, columns=["Data"])
        df.to_excel(self.filename, index=False)
        print(f"Данные успешно экспортированы в файл {self.filename}")
