import json
import psycopg2
from config import database, user, password, host
from src.get_vacancies import load_vacancies

# Чтение данных из JSON файла
with open('companies_id.json') as json_file:
    data = json.load(json_file)

with psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
) as conn:
    with conn.cursor() as cur:
        # удаляем таблицу companies, если она уже существует
        cur.execute("DROP TABLE IF EXISTS companies")
        # Создаем таблицу companies, если она не существует
        cur.execute("CREATE TABLE companies (company_id INT PRIMARY KEY, company_name VARCHAR(255) )")

        # Добавляем данные из JSON файла в таблицу
        for company_name, company_id in data[0].items():
            cur.execute("INSERT INTO companies (company_id, company_name) VALUES (%s, %s)", (company_id, company_name))

        # Фиксируем изменения
        conn.commit()

        # удаляем таблицу vacancies, если она уже существует
        cur.execute("DROP TABLE IF EXISTS vacancies")
        # создаём в postgres sql таблицу вакансий
        cur.execute("""
                CREATE TABLE vacancies (
                    company varchar (100),
                    job_title varchar(100),
                    link_to_vacancy varchar(100),
                    salary_from int,
                    salary_to int,
                    description text,
                    requirement text); 
                    """)
        # Добавляем данные о вакансиях в переменную vacancies_list и на её основе добавляем записи в  таблицу vacancies
        vacancies_list = load_vacancies()
        print(vacancies_list)
        for vacancy in vacancies_list:
            cur.execute(
                'INSERT INTO vacancies (company, job_title, link_to_vacancy, salary_from, salary_to, '
                'description, requirement) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (vacancy.get('company'), vacancy.get('job_title'), vacancy.get('link_to_vacancy'),
                 vacancy.get('salary_from'), vacancy.get('salary_to'), vacancy.get('description'),
                 vacancy.get('requirement')))
        # Фиксируем изменения
        conn.commit()

        cur.execute("SELECT * FROM vacancies")
        rows = cur.fetchall()
        for row in rows:
            print(row)

# Закрытие курсора
cur.close()

# Закрытие соединения
conn.close()
