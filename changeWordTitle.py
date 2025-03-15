import os
from bs4 import BeautifulSoup

# Папка с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Функция для замены слова в теге <title>
def replace_title_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Находим тег <title>
        title_tag = soup.find('title')
        
        if title_tag:
            # Заменяем слово 'dieInkasso' на 'Berginkasso' в тексте тега title
            title_tag.string = title_tag.string.replace('dieInkasso', 'Berginkasso')

            # Сохраняем изменения
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            print(f"Тег <title> обновлен в файле: {file_path}")
        else:
            print(f"Тег <title> не найден в файле: {file_path}")

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Проходим по всем HTML-файлам в папке и заменяем слово в теге <title>
for root, _, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            replace_title_in_file(file_path)

print("Замена слова в тегах <title> завершена на всех страницах.")
