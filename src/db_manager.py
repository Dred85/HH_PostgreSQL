import psycopg2


class DBManager:
    def __init__(self, database, user, password, port, host):
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.host = host
        self.conn = psycopg2.connect(database=self.database, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании.
        :return:
        """
        query = """
                SELECT company, COUNT(*)
                FROM vacancies 
                GROUP BY company
                """
        self.cur.execute(query)
        return {row[0]: row[1] for row in self.cur.fetchall()}

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        query = """
                SELECT company, job_title, salary_from, link_to_vacancy
                FROM vacancies
                """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        :return:
        """
        query = """
                SELECT AVG(salary_from)
                FROM vacancies
                """
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        query = """
                SELECT job_title, salary_from
                FROM vacancies
                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :return:
        """
        query = """
                SELECT * FROM vacancies
                WHERE LOWER(job_title) LIKE %s
                """
        self.cur.execute(query, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()


