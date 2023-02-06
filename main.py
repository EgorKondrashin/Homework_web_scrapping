import time

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import json

ua = UserAgent()
data = []


def get_source_html():
    for i in range(0, 40):
        response = requests.get(
            url=f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={i}",
            headers={"user-agent": f"{ua.random}"}
        )
        soup = BeautifulSoup(response.text, "lxml")
        source_list = soup.find_all("div", class_="serp-item")

        for source_vacancy in source_list:
            try:
                vacancy_salary = source_vacancy.find("div", class_="vacancy-serp-item-body__main-info").find("div", class_="")\
                    .find("div", class_="bloko-v-spacing bloko-v-spacing_base-1").next_sibling.text
                vacancy_name = source_vacancy.find("a", class_="serp-item__title").text
                vacancy_url = source_vacancy.find("a", class_="serp-item__title").get("href")
                vacancy_company = source_vacancy.find("div", class_="vacancy-serp-item__meta-info-company").find("a").text
                vacancy_address = source_vacancy.find("div", class_="vacancy-serp-item__info")\
                    .find("div", class_="bloko-v-spacing bloko-v-spacing_base-3").previous_sibling.text
                vacancy_address = vacancy_address.split(",")[0]
                vacancy_short_description_list = source_vacancy.find("div", class_="g-user-content")\
                    .find_all("div", class_="bloko-text")
                vacancy_description_list = []
                for vacancy_description in vacancy_short_description_list:
                    vacancy_description_list.append(vacancy_description.text)
                vacancy_short_description = "".join(vacancy_description_list)
                if "USD" in vacancy_salary and "Django" in vacancy_short_description \
                        and "Flask" in vacancy_short_description:
                    data.append(
                        {
                            "Вакансия": vacancy_name,
                            "Ссылка": vacancy_url,
                            "Зарплата": vacancy_salary.remove("\u202f", " "),
                            "Город": vacancy_address,
                            "Компания": vacancy_company,
                            "Краткое описание": vacancy_short_description
                        }
                    )
                    print(f"Вакансия: {vacancy_name} была добавлена")
            except AttributeError:
                continue
        print(f"[INFO]: обработана {i+1}-ая страница из 40")
        time.sleep(3)
    with open("data.json", "a") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    get_source_html()


if __name__ == '__main__':
    main()
