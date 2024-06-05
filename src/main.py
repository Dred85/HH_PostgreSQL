from db_manager import DBManager
from src.config import config
from utils import create_db


def main():
    # Получаем параметры подключения к базе данных из файла database.ini
    params = config()
    # Создаем таблицы companies и vacancies
    create_db()
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
