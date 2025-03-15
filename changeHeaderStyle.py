import os
from bs4 import BeautifulSoup

# Папка с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Путь к главному index.html
main_index_path = os.path.join(folder_path, 'index.html')

# Функция для извлечения стилей из блока <style id="astra-theme-css-inline-css">
def get_styles_from_main_index():
    try:
        with open(main_index_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Находим блок <style id="astra-theme-css-inline-css">
        style_tag = soup.find('style', id='astra-theme-css-inline-css')
        
        if style_tag:
            return style_tag.string
        else:
            print("Не найден <style id='astra-theme-css-inline-css'> в главном index.html.")
            return None
    except Exception as e:
        print(f"Ошибка при извлечении стилей из главного index.html: {e}")
        return None

# Функция для добавления стиля в конец блока <style> на других страницах
def add_style_to_page(file_path, new_style):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Находим блок <style id="astra-theme-css-inline-css">
        style_tag = soup.find('style', id='astra-theme-css-inline-css')

        if style_tag:
            # Проверяем, есть ли уже необходимый стиль
            if '.menu-item.current-menu-item > .menu-link {color:#e59385 !important;}' not in style_tag.string:
                # Добавляем стиль в конец
                style_tag.string += '\n.menu-item.current-menu-item > .menu-link {color:#e59385 !important;}'
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                print(f"Стиль добавлен в файл: {file_path}")
            else:
                print(f"Стиль уже присутствует в файле: {file_path}")
        else:
            print(f"Не найден <style id='astra-theme-css-inline-css'> в файле: {file_path}")

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Получаем стили из главного index.html
styles_from_main = get_styles_from_main_index()

if styles_from_main:
    # Проходим по всем HTML-файлам в папке и добавляем стиль, если необходимо
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if file_path != main_index_path:
                    add_style_to_page(file_path, styles_from_main)

    print("Добавление стилей завершено на всех страницах, кроме исходного index.html.")
else:
    print("Не удалось получить стили из главного index.html.")