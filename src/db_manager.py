import psycopg2
from typing import Any


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self, db_name: str, params: dict[str, Any]) -> None:
        self.db_name = db_name
        self.params = params

    def __connect_database(self):
        """Подключение к базе данных"""
        return psycopg2.connect(dbname=self.db_name, **self.params)

    def get_companies_and_vacancies_count(self):
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute(
                """SELECT employers.employer_name, COUNT(*)
                FROM vacancies JOIN employers USING(employer_id)
                GROUP BY employers.employer_name;""")
            vacs_counter = cur.fetchall()

        for employer in vacs_counter:
            print(f"{employer[0]}: {employer[1]} вакансий")

        conn.close()

    def get_all_vacancies(self):
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("""SELECT employers.employer_name, vacancy_name, salary_from, salary_to, vacancies.url
            FROM vacancies JOIN employers USING(employer_id);""")
            vacs_data = cur.fetchall()

        for vac in vacs_data:
            if vac[2] == 0.0 and vac[3] == 0.0:
                print(f"♥{vac[0]}♥, вакансия: {vac[1]}\nЗарплата: не указана. Ссылка: {vac[4]}\n")
            elif vac[3] == 0.0:
                print(f"♥{vac[0]}♥, вакансия: {vac[1]}\nЗарплата: от {vac[2]}. Ссылка: {vac[4]}\n")
            elif vac[2] == 0.0 :
                print(f"♥{vac[0]}♥, вакансия: {vac[1]}\nЗарплата: до {vac[3]}. Ссылка: {vac[4]}\n")
            else:
                print(f"♥{vac[0]}♥, вакансия: {vac[1]}\nЗарплата: {vac[2]} - {vac[3]}. Ссылка: {vac[4]}\n")

        conn.close()

    def get_avg_salary(self):
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies;""")
            salary_from = round(cur.fetchone()[0])

            cur.execute("""SELECT AVG(salary_to) FROM vacancies;""")
            salary_to = round(cur.fetchone()[0])

        print(f"Средняя зарплата: {salary_from} - {salary_to}")

        conn.close()

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass