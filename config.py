import os

# Абсолютный путь до ROOT_DIR
ROOT_DIR = os.path.dirname(__file__)
path_to_file_new = os.path.join(ROOT_DIR, 'data', 'vacancies_all.json')
path_to_file_update = os.path.join(ROOT_DIR, 'data', 'vacancies_update.json')