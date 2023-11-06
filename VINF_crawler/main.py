import requests
from bs4 import BeautifulSoup
import re
import time


# Press the green button in the gutter to run the script.

def find_details(html):
    links = []
    pattern = '/.*/details.*/["\']'
    matches = set(re.findall(pattern, html))
    for match in matches:
        links.append("https://www.comics.org" + match[:-1])
    return links


def visit_website(url, file):
    time.sleep(1)
    try:

        response = requests.get(url)

        if response.status_code == 200:

            html = response.text
            # print(html)

            file.write(response.url + "\n")
            try:
                file.write(html)
            except Exception as e:
                print(f"An unexpected exception occurred: {e}", "url:", response.url)
            file.write("-----\n")
            return html
        else:
            print(f"Failed to retrieve {url}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def id_keeper(number):
    try:
        with open("id_keeper.txt", 'r') as file:
            content = file.read()
            if not content:
                print("The file is empty.")
            else:
                number = int(content)
    except FileNotFoundError:
        print("File not found. Creating a new file.")
        with open("id_keeper.txt", 'w') as file:
            file.write(str(number))

    return number


def id_write(number):
    with open("id_keeper.txt", 'w') as file:
        file.write(str(number))


if __name__ == '__main__':
    url_template = 'https://www.comics.org/series/{number}/'
    number = 64945
    number = id_keeper(number)
    crawl_size = 1
    start_time = time.time()
    with open("crawled_websites.txt", 'a', encoding="utf-8") as file:
        for i in range(crawl_size):
            if i % 25 == 0:
                print("Only %s to go" % (crawl_size - i))
            url = url_template.format(number=number)
            html = visit_website(url, file)
            for link in find_details(html):
                visit_website(link, file)
            number += 1

    id_write(number)
    end_time = time.time()
    print("Elapsed time", end_time - start_time)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
