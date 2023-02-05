import os
import datetime
import requests
from lxml import html


HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//a[contains(@class,"kicker")]/@href'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY ='//div[@class="html-content"]//text()'


def get_title(link):
    #separamos por "/" y nos quedamos con el ultimo que elemento
    url = link.split('/')[-1]
    #separamos por "-" y eliminamos el ultimo elemento
    title_list=url.split('-')[:-1]
    #Unimos lo anterior
    return " ".join(title_list)


def parse_notice(link, today):
    try:
        response = requests.get(link, timeout=10)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = get_title(link)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                print("as")
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as file:
                file.write(title)
                file.write('\n\n')
                file.write(summary)
                file.write('\n\n')
                for post in body:
                    file.write(post)
                    file.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as value_error:
        print(value_error)

def parse_home():
    try:
        response = requests.get(HOME_URL, timeout=10)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as value_error:
        print(value_error)


def run():
    parse_home()


if __name__ == "__main__":
    run()
