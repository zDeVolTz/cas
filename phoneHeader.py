import os
from bs4 import BeautifulSoup

# Папка с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Путь к главному index.html
main_index_path = os.path.join(folder_path, 'index.html')

# Функция для извлечения <li> из главного index.html
def get_new_menu_items():
    try:
        with open(main_index_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Ищем только <li> с нужным классом внутри header
        custom_menu_items = soup.select('header li.ast-masthead-custom-menu-items.button-custom-menu-item')

        if not custom_menu_items:
            print("Не найдено элементов <li> в header главного index.html.")
            return None

        return custom_menu_items  # Возвращаем список объектов BeautifulSoup
    except Exception as e:
        print(f"Ошибка при извлечении меню из главного index.html: {e}")
        return None

# Функция для замены только нужных <li> в файле
def replace_header_menu_items(file_path, new_menu_items):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Ищем старые <li> с тем же классом
        old_menu_items = soup.select('header li.ast-masthead-custom-menu-items.button-custom-menu-item')

        if not old_menu_items:
            print(f"Не найдено меню в файле: {file_path}")
            return

        # Заменяем каждый старый <li> на новый
        for old, new in zip(old_menu_items, new_menu_items):
            old.replace_with(new)

        # Записываем обновленный HTML обратно в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        
        print(f"Меню заменено в файле: {file_path}")

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Получаем новые <li> из главного index.html
new_menu_items = get_new_menu_items()

if new_menu_items:
    # Проход по всем HTML-файлам и замена нужных <li>
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                replace_header_menu_items(file_path, new_menu_items)

    print("Замена элементов <li> завершена на всех страницах.")
else:
    print("Не удалось получить элементы <li> из главного index.html.")
