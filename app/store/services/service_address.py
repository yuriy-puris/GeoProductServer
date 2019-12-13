import requests
import time
from time import sleep

from bs4 import BeautifulSoup
from lxml import html
import lxml.etree

from . import service_headers
from ..models import Address

def parser_address_moyo():
    url = 'https://www.moyo.ua/trade_network.html'
    response = requests.get(url, headers=service_headers.headers['2'])
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    contacts = soup.select('div.shopinfo_text > p:first-child')
    address = [i.getText() for i in contacts]
    for item in address:
        model_address = Address(
            address = item,
            shop_id_id = 2
        )
        model_address.save()
    return address

def parser_address_allo():
    url = 'https://allo.ua/ua/offline_stores/'
    response = requests.get(url, headers=service_headers.headers['2'])
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    
    contacts_part_one = soup.select('div.offline-stores-bottom-wrap > .offline-stores-bottom-wrap-h2')
    address_part_one = [i.getText().strip() for i in contacts_part_one]

    contacts_part_two = soup.find('div', class_='offline-stores-bottom-wrap')
    contacts_part_two_tables = contacts_part_two.find_all('table')

    address_part_two = []
    for item in contacts_part_two_tables:
        item_td_common = item.find_all('td', class_=lambda x: x == 'cell')
        result_address = [td.getText().strip() for td in item_td_common if "phone" not in td['class']]
        address_part_two.append(result_address)

    assigned_address = []

    for i in range(len(address_part_one)):
        for item in address_part_two[i]:
            address_item = address_part_one[i] + ', ' + item
            assigned_address.append(address_item)
    
    for item in assigned_address:
        model_address = Address(
            address = item,
            shop_id_id = 4
        )
        model_address.save()
    return assigned_address

def parser_address_foxtrot():
    url = 'https://www.foxtrot.com.ua/ru/stores'
    # 'https://www.foxtrot.com.ua/ru/stores/liststores?city=38053711&_=1575146916266'
    response = requests.get(url, headers=service_headers.headers['2'])
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    
    contact_option = soup.select('.address-wrapper #city option')

    for option in contact_option:
        value = option.get('value')
        text = option.getText()
        url_address = 'https://www.foxtrot.com.ua/ru/stores/liststores?city='+value
        response = requests.get(url_address, headers=service_headers.headers['2'])
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        shops_item = soup.select('.shops__item .item__info:nth-of-type(2) .item__info_text')
        for address in shops_item:
            full_address = text + ', ' + address.getText().strip()
            model_address = Address(
                address = full_address,
                shop_id_id = 5
            )
            model_address.save()
        time.sleep(5)






# def parser_address_psshop():
#     url = 'https://pcshop.ua/contact'

# def parser_address_deshevle():
#     url = 'https://www.deshevle-net.com.ua/'

# def parser_address_tt():
#     url = 'https://tt.ua/kontakti'