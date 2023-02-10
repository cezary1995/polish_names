from typing import Union

import requests
from bs4 import BeautifulSoup


def load_polish_names():
    with open('imiona_polskie.txt', 'r', encoding='UTF-8') as file:
        return file.read().splitlines()


POLISH_NAMES = load_polish_names()


# Remove polish signs from names
def get_names_without_polish_signs() -> list:
    polish_signs = str.maketrans('ąĄćĆęĘłŁńŃóÓśŚźŹżŻ', 'aAcCeElLnNoOsSzZzZ')
    polish_names_urls = []
    for name in POLISH_NAMES:
        name = name.translate(polish_signs)
        polish_names_urls.append(name)
    return polish_names_urls


# Generate url adres with specific endpoint
def get_request(name: str) -> str:
    return f"https://www.znaczenie-imion.net/a/{name}.html"


# Get meaning name paragraphs from webpage
def get_meaning_name(content) -> Union[str, None]:
    meaning_list = []
    paragraph = 1
    for data in content.find_all('p'):
        if 1 < paragraph < 5:
            meaning_list.append(data.getText())
        paragraph += 1
    meaning_name = ' '.join(meaning_list)
    return meaning_name


def get_origin_name(content):
    h3 = content.find("h3")
    return h3.find("p").text


def get_page_content(req):
    soup = BeautifulSoup(req.text, 'html.parser')
    content = soup.find("div", class_="thecontent")
    return content


# Return list of dictionaries containing origin and meaning polish names
def get_data_name() -> list:
    list_of_data = []
    for name in get_names_without_polish_signs():
        data_names = {}
        r = requests.get(get_request(name))
        status_code = r.status_code
        data_names['name'] = name.capitalize()
        if status_code == 200:
            content = get_page_content(r)

            data_names['origin_name'] = content.find('p').text
            data_names['meaning_name'] = get_meaning_name(content)
        else:
            data_names['origin_name'] = None
            data_names['meaning_name'] = None

        list_of_data.append(data_names)
    return list_of_data


if __name__ == '__main__':
    print(get_data_name())
