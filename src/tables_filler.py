import psycopg2

from typing import Any


def enter_data_into_tables(db_name: str, params: dict[str, Any], employers_data: dict[str, Any],
                           vacancies_data: list[dict[str, Any]]) -> None:
    """Заполнение таблиц данными о работадателях и вакансиях"""

    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        # заполняем таблицу employers
        cur.execute("""
            INSERT INTO employers (employer_name, employer_url)
            VALUES (%s, %s)
            RETURNING employer_id;""",
                    (employers_data.get('name'), employers_data.get('url'))
                    )

        # заполняем таблицу vacancies
        employer_id = cur.fetchone()[0]

        for vacancy_data in vacancies_data:
            name = vacancy_data.get("name")
            sal_from = vacancy_data.get("salary_from")
            sal_to = vacancy_data.get("salary_to")
            req = vacancy_data.get("requirement")
            resp = vacancy_data.get("responsibility")
            url = vacancy_data.get("url")

            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO vacancies (employer_id, vacancy_name, salary_from, salary_to, requirement, responsibility, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                    (employer_id, name, sal_from, sal_to, req, resp, url)
            )

    conn.commit()
    conn.close()
