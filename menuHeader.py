import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Папка с HTML-файлами
folder_path = r'C:/OSPanel/domains/test/gits/project/dieinkasso/www.dieinkasso.ch'

# Путь к главному index.html
main_index_path = os.path.join(folder_path, 'index.html')

# Функция для извлечения содержимого <div class="main-navigation"> из главного index.html
def get_new_navigation_content():
    try:
        with open(main_index_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        new_navigation_div = soup.select_one('div.main-navigation')

        if not new_navigation_div:
            print("Не найден <div class='main-navigation'> в главном index.html.")
            return None

        return new_navigation_div
    except Exception as e:
        print(f"Ошибка при извлечении навигации из главного index.html: {e}")
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

# Функция для нормализации пути (для корректного сравнения)
def normalize_path(path):
    return os.path.normpath(path).replace("\\", "/")

# Функция для замены содержимого <div class="main-navigation"> в файле
def replace_navigation_content_in_file(file_path, new_navigation_content):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Изменено: теперь выбираем все блоки div.main-navigation
        old_navigation_divs = soup.select('div.main-navigation')

        if not old_navigation_divs:
            print(f"Не найден <div class='main-navigation'> в файле: {file_path}")
            return

        relative_prefix = get_relative_path(file_path)

        # Получаем текущий путь для поиска активного пункта меню
        current_path = os.path.relpath(file_path, folder_path)
        current_path = normalize_path(current_path)  # Приводим к нормальному виду

        # Применяем изменения ко всем найденным блокам
        for old_navigation_div in old_navigation_divs:
            # Клонируем новый контент и заменяем старый
            new_navigation_clone = BeautifulSoup(str(new_navigation_content), 'html.parser').div

            # Обработка всех ссылок внутри блока
            for li_tag in new_navigation_clone.find_all('li'):
                a_tag = li_tag.find('a')
                if a_tag:
                    href = a_tag.get('href')

                    # Проверка на активную страницу (сравниваем относительные пути)
                    if href:
                        # Приводим href к нормальному виду
                        href = normalize_path(href)

                        # Проверяем, совпадает ли путь в ссылке с текущим путем
                        if href == current_path:
                            # Добавляем класс current-menu-item, если его нет
                            existing_classes = li_tag.get('class', [])
                            if 'current-menu-item' not in existing_classes:
                                li_tag['class'] = existing_classes + ['current-menu-item']

                            # Если у li есть вложенный ul, добавляем класс родительскому li
                            parent_li = li_tag.find_parent('li')
                            if parent_li:
                                parent_existing_classes = parent_li.get('class', [])
                                if 'current-menu-item' not in parent_existing_classes:
                                    parent_li['class'] = parent_existing_classes + ['current-menu-item']

                    # Преобразуем все остальные href в относительные
                    if href and not is_valid_url(href) and not href.startswith('tel:'):
                        # Если ссылка не абсолютная, добавляем относительный префикс
                        a_tag['href'] = relative_prefix + href

            # Очищаем старый блок и вставляем новый
            old_navigation_div.clear()
            old_navigation_div.append(new_navigation_clone)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Навигация заменена в файле: {file_path}")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

# Получаем новый контент навигации
new_navigation_content = get_new_navigation_content()

if new_navigation_content:
    # Проходим по всем HTML-файлам в папке и заменяем навигацию
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if file_path != main_index_path:
                    replace_navigation_content_in_file(file_path, new_navigation_content)

    print("Замена навигации завершена на всех страницах, кроме исходного index.html.")
else:
    print("Не удалось получить <div class='main-navigation'> из главного index.html.")
