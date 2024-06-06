import json

import requests

from config_root import path_to_file_vacancies, path_to_file_companies_id

# Чтение данных из JSON файла companies_id.json c интересующими компаниями
with open(path_to_file_companies_id) as json_file:
    companies = json.load(json_file)


def load_vacancies():
    vacancies = []

    for company in companies[0].keys():
        url = "https://api.hh.ru/vacancies"
        params = {'text': company, 'per_page': 100}
        data = requests.get(url, params=params)

        if data.status_code == 200:
            json_data = data.json()
            for item in json_data['items']:
                job_title = item['name']
                link_to_vacancy = item['alternate_url']
                salary = item['salary']
                if salary:
                    salary_from = salary.get('from')
                    salary_to = salary.get('to')
                else:
                    salary_from = None
                    salary_to = None

                description = item['snippet']['responsibility']
                requirement = item['snippet']['requirement']

                vacancies.append({
                    "company": company,
                    "job_title": job_title,
                    "link_to_vacancy": link_to_vacancy,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "description": description,
                    "requirement": requirement
                })
        else:
            print(f"Ошибка {data.status_code}")
    return vacancies



# Загружаем вакансии в JSON файл, для наглядности выгруженных вакансий
vacancies = load_vacancies()
with open(path_to_file_vacancies, 'w') as file:
    json.dump(vacancies, file, ensure_ascii=False, indent=4)

