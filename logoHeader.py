import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Папка с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Путь к главному index.html
main_index_path = os.path.join(folder_path, 'index.html')

# Функция для извлечения содержимого <span class="site-logo-img"> из главного index.html
def get_new_logo_content():
    try:
        with open(main_index_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        new_logo_span = soup.select_one('header span.site-logo-img')

        if not new_logo_span:
            print("Не найден <span class='site-logo-img'> в header главного index.html.")
            return None

        return new_logo_span
    except Exception as e:
        print(f"Ошибка при извлечении логотипа из главного index.html: {e}")
        return None

# Функция для преобразования пути к файлу в относительный путь к корню сайта
def get_relative_path(file_path):
    relative_path = os.path.relpath(file_path, folder_path)
    depth = relative_path.count(os.sep)
    return "../" * depth if depth > 0 else ""

# Функция для проверки корректности ссылки
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) or url.startswith('/')

# Функция для замены содержимого <span class="site-logo-img"> в файле, сохраняя <a>
def replace_logo_content_in_file(file_path, new_logo_content):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')
        old_logo_spans = soup.select('header span.site-logo-img')

        if not old_logo_spans:
            print(f"Не найден <span class='site-logo-img'> в файле: {file_path}")
            return

        relative_prefix = get_relative_path(file_path)

        for old_logo_span in old_logo_spans:
            old_a_tag = old_logo_span.find('a')
            old_href = old_a_tag.get('href') if old_a_tag else None
            
            new_logo_clone = BeautifulSoup(str(new_logo_content), 'html.parser').span
            new_a_tag = new_logo_clone.find('a')
            
            if old_a_tag and old_href:
                if not is_valid_url(old_href):
                    old_href = relative_prefix + "index.html"
                if new_a_tag:
                    new_a_tag['href'] = old_href
                else:
                    new_a_tag = old_a_tag
                    new_logo_clone.append(new_a_tag)
            elif new_a_tag:
                new_a_tag['href'] = relative_prefix + "index.html"
            
            old_logo_span.clear()
            old_logo_span.append(new_logo_clone)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Логотип заменён в файле: {file_path}")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

new_logo_content = get_new_logo_content()

if new_logo_content:
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if file_path != main_index_path:
                    replace_logo_content_in_file(file_path, new_logo_content)

    print("Замена логотипов завершена на всех страницах, кроме исходного index.html.")
else:
    print("Не удалось получить <span class='site-logo-img'> из главного index.html.")