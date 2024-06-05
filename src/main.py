from db_manager import DBManager
from src.config import config
import psycopg2
from src.get_vacancies import load_vacancies, companies


def main():
    params = config()

    with psycopg2.connect(
        **params
    ) as conn:
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

    # Создаем экземпляр класса DBManager
    db_manager = DBManager('postgres', **params)
    while True:
        print(f'''Запрос к базе данных: 
                  1  Список всех компаний и количество вакансий у каждой компании
                  2  Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
                  3  Средняя зарплата по вакансиям
                  4  Список всех вакансий, у которых зарплата выше средней по всем вакансиям
                  5  Список всех вакансий, в названии которых содержатся запрашиваемое слово,
                  Для выхода нажмите q''')
        user_request = input('Ввод: ').lower().strip()
        if user_request == '1':
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании: {companies_vacancies_count}")
        elif user_request == '2':
            vacancy_list = db_manager.get_all_vacancies()
            print(
                f"Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию: {vacancy_list}")
        elif user_request == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплату по вакансиям: {avg_salary}")
        elif user_request == '4':
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(
                f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: {vacancies_with_higher_salary}")
        elif user_request == '5':
            user_input = input(f'Введите слово:')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"список всех вакансий, в названии которых содержатся {user_input}: {vacancies_with_keyword}")
        elif user_request == 'q':
            break
        else:
            print(f"Введён неверный запрос")


if __name__ == "__main__":
    main()
