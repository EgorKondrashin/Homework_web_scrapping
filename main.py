import time

import requests
from bs4 import BeautifulSoup
import json

headers = {'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
           'Accept-Language': 'ru-RU,ru;q=0.9',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'same-origin',
           'Sec-Fetch-User': '?1',
           'Cache-Control': 'max-age=0',
           'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
           'sec-ch-ua-mobile': '?0'}
data = []


def get_source_html():
    for i in range(0, 40):
        response = requests.get(
            url=f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={i}",
            headers=headers
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
