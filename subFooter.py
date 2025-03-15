import os
from bs4 import BeautifulSoup

# Папка с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Путь к главному index.html
main_index_path = os.path.join(folder_path, 'index.html')

# Функция для извлечения содержимого блока <div> с классом 'fl-node-5d430ae263efe' из главного index.html
def get_content_from_main_index():
    try:
        with open(main_index_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Находим блок <div> с классом 'fl-node-5d430ae263efe'
        target_div = soup.find('div', class_='fl-node-5d430ae263efe')
        
        if target_div:
            return target_div
        else:
            print("Не найден <div class='fl-node-5d430ae263efe'> в главном index.html.")
            return None
    except Exception as e:
        print(f"Ошибка при извлечении содержимого из главного index.html: {e}")
        return None

# Функция для замены содержимого блока <div class='fl-node-5d430ae263efe'> на других страницах
def replace_content_in_page(file_path, new_content):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Находим все блоки <div> с классом 'fl-node-5d430ae263efe'
        target_divs = soup.find_all('div', class_='fl-node-5d430ae263efe')

        if target_divs:
            for target_div in target_divs:
                # Заменяем содержимое блока на новое
                target_div.clear()
                target_div.append(new_content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            print(f"Содержимое блока <div class='fl-node-5d430ae263efe'> заменено в файле: {file_path}")
        else:
            print(f"Не найден <div class='fl-node-5d430ae263efe'> в файле: {file_path}")

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Получаем содержимое блока из главного index.html
new_content_from_main = get_content_from_main_index()

if new_content_from_main:
    # Проходим по всем HTML-файлам в папке и заменяем содержимое блока
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if file_path != main_index_path:
                    replace_content_in_page(file_path, new_content_from_main)

    print("Замена содержимого блока завершена на всех страницах, кроме исходного index.html.")
else:
    print("Не удалось получить содержимое блока из главного index.html.")