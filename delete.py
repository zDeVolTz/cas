import os
from bs4 import BeautifulSoup

# Укажите путь к папке с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Старые теги и классы, которые нужно удалить
tags_to_remove = [
    ('div', {'class': 'gtranslate_wrapper'}),
    ('link', {'id': 'astra-addon-megamenu-dynamic-css'}),
    ('style', {'id': 'astra-addon-megamenu-dynamic-inline-css'})
]

# Функция для удаления элементов из HTML
def remove_elements_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Удаляем указанные элементы
        for tag, attributes in tags_to_remove:
            elements = soup.find_all(tag, attributes)
            for element in elements:
                element.decompose()

        # Записываем изменённое содержимое обратно в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"Обработан файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Проход по всем HTML-файлам в папке
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            remove_elements_from_file(file_path)

print("Удаление завершено на всех страницах.")
