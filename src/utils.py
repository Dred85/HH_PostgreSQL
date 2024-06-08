import psycopg2
from src.get_vacancies import load_vacancies, companies


def create_db(database_name, params):
    # Подключаемся к базе данных
    conn = psycopg2.connect(dbname="postgres", **params)
    # Устанавливаем autocommit, чтобы изменения сохранялись сразу же
    conn.autocommit = True
    # Получаем курсор
    cur = conn.cursor()
    # Удаляем базу данных, если она уже существует
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    #  Создаем базу данных
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    with psycopg2.connect(dbname=database_name, **params) as conn:
        with conn.cursor() as cur:
            # удаляем таблицу companies, если она уже существует
            cur.execute("DROP TABLE IF EXISTS companies")
            # Создаем таблицу companies, если она не существует
            cur.execute("CREATE TABLE companies (company_id INT PRIMARY KEY, company_name VARCHAR(255) )")

            # Добавляем данные из JSON файла в таблицу
            for company_name, company_id in companies[0].items():
                cur.execute("INSERT INTO companies (company_id, company_name) VALUES (%s, %s)",
                            (company_id, company_name))

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
            for vacancy in vacancies_list:
                cur.execute(
                    'INSERT INTO vacancies (company, job_title, link_to_vacancy, salary_from, salary_to, '
                    'description, requirement) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (vacancy.get('company'), vacancy.get('job_title'), vacancy.get('link_to_vacancy'),
                     vacancy.get('salary_from'), vacancy.get('salary_to'), vacancy.get('description'),
                     vacancy.get('requirement')))
            # Фиксируем изменения
            conn.commit()

            cur.execute("SELECT * FROM vacancies INNER JOIN companies ON vacancies.company=companies.company_name;")
            rows = cur.fetchall()
            for row in rows:
                print(*row)

    # Закрытие курсора
    cur.close()

    # Закрытие соединения
    conn.close()
