import requests

from bs4 import BeautifulSoup
from lxml import html
import lxml.etree

from . import service_headers
  
COUNT_PRODUCTS_SHOP = 3

SHOPS_PRODUCT_LIST_CLASSES = {
  2: 'product-tile_container',
  4: 'category-products',
  5: 'listing-container'
}

def get_response(url):
  response = requests.get(url, headers=service_headers.headers['2'])
  return response.text

def get_category(shop_id, html):
  soup = BeautifulSoup(html, 'html.parser')
  soup.prettify()
  content_wrap = soup.find(True, class_=SHOPS_PRODUCT_LIST_CLASSES[shop_id])
  return content_wrap

def parse_product_list(shop_id, content):
  if shop_id == 2:
    return get_product_list_shop_2(shop_id, content)
  if shop_id == 4:
    return get_product_list_shop_4(shop_id, content)
  if shop_id == 5:
    return get_product_list_shop_5(shop_id, content)

def get_product_list_shop_4(shop_id, content):
  grid_list = content.find_all('li', class_='item')
  products = []

  for item in grid_list[:COUNT_PRODUCTS_SHOP]:
    img_block = item.find('div', class_='item-picture-blk')
    img = img_block.find('img').attrs
    img_url = img['data-original']

    title = item.find_all('div', class_='product-name-container')[0].text.strip()
    # price = item.find_all('span', class_='price')
    # price_new = item.find('span', class_='new_sum').text.strip().replace(u"\xa0", u".")
    price = item.find('span', class_='sum').text.strip().replace(u"\xa0", u".")
    # print(item.find('span', class_='new_sum'))
    product = {
      'shop_id': shop_id,
      'img':   img_url,
      'title': title,
      'price': price
    }
    products.append(product)

  return products

def get_product_list_shop_5(shop_id, content):
  grid_list = content.find_all('div', class_=['listing-item', 'product-item', 'simple'])
  products = []

  for item in grid_list[:COUNT_PRODUCTS_SHOP]:
    item_attrs = item.attrs
    item_img = item.find('img', class_='lazy-category').attrs
    img = item_img['data-src']
    title = item_attrs['data-title']
    price = item_attrs['data-price']

    product = {
      'shop_id': shop_id,
      'img':   img,
      'title': title,
      'price': price
    }

    products.append(product)
  return products

def get_product_list_shop_2(shop_id, content):
  grid_list = content.find_all('section', class_='product-tile_product')
  products = []

  for item in grid_list[:COUNT_PRODUCTS_SHOP]:
    item_attrs = item.attrs
    img_attrs = item.find('figure', class_='goods_image').attrs
    img = img_attrs['data-imagesrc']
    title = item_attrs['data-name']
    price = item_attrs['data-price']

    product = {
      'shop_id': shop_id,
      'img':   img,
      'title': title,
      'price': price
    }

    products.append(product)
  return products


def parse_shop(shop_id, url):
  html = get_response(url)
  content_products = get_category(shop_id, html)
  parse_products = parse_product_list(shop_id, content_products)
  return parse_products