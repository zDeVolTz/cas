import os
from bs4 import BeautifulSoup

# Укажите путь к папке с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Путь к главному индексу (где футер уже имеется)
main_index_path = os.path.join(folder_path, 'index.html')

# Функция для извлечения футера из главного индекса
def get_footer_from_main_index():
    try:
        with open(main_index_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Находим футер, можно по классу или уникальной части кода
        old_footer_start = '<footer class="site-footer"'
        old_footer_end = '</footer>'

        if old_footer_start in content and old_footer_end in content:
            start_index = content.find(old_footer_start)
            end_index = content.find(old_footer_end) + len(old_footer_end)
            footer = content[start_index:end_index]
            return footer
        else:
            print("Футер не найден в главном индексе.")
            return None
    except Exception as e:
        print(f"Ошибка при чтении главного индекса: {e}")
        return None

# Функция для замены футера в HTML-файле
def replace_footer_in_file(file_path, footer):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Находим старый футер и заменяем его новым
        old_footer_start = '<footer class="site-footer"'
        old_footer_end = '</footer>'

        if old_footer_start in content and old_footer_end in content:
            # Если футер найден, заменяем его
            start_index = content.find(old_footer_start)
            end_index = content.find(old_footer_end) + len(old_footer_end)
            content = content[:start_index] + footer + content[end_index:]

            # Записываем изменённое содержимое обратно в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Футер заменен в файле: {file_path}")
        else:
            print(f"Футер не найден в файле: {file_path}")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Функция для замены ссылок в футере с учетом старых ссылок страницы
def replace_links_in_footer(footer, file_path):
    footer_soup = BeautifulSoup(footer, 'html.parser')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Извлекаем все ссылки из текущего футера страницы
        page_soup = BeautifulSoup(content, 'html.parser')
        old_links = {a_tag.string: a_tag['href'] for a_tag in page_soup.find_all('a')}

        # Заменяем все ссылки в новом футере на старые из текущей страницы
        for a_tag in footer_soup.find_all('a'):
            if a_tag.string in old_links:
                a_tag['href'] = old_links[a_tag.string]

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

    return str(footer_soup)

# Получаем футер из главного индекса
footer = get_footer_from_main_index()

if footer:
    # Проход по всем HTML-файлам в папке и замена футера в файлах внутри вложенных папок
    for root, dirs, files in os.walk(folder_path):
        if root == folder_path:
            files = [file for file in files if file != 'index.html']

        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                # Заменяем ссылки в футере на старые из текущей страницы
                updated_footer = replace_links_in_footer(footer, file_path)
                # Заменяем футер в файле
                replace_footer_in_file(file_path, updated_footer)

    print("Замена футера завершена на всех страницах.")
else:
    print("Не удалось получить футер из главного индекса.")
