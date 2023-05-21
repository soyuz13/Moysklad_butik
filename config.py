from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv('USR')
PASS = os.getenv('PASS')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_BASE = os.getenv('DB_BASE')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))

# print(USER, PASS)

MAIN_URL = 'https://online.moysklad.ru/api/remap/1.2/'
URL_ORGANIZATION = MAIN_URL + 'entity/organization'
URL_PRICETYPE = MAIN_URL + 'context/companysettings/pricetype'
URL_CONTRAGENT = MAIN_URL + 'entity/counterparty/'
URL_DISCOUNT = MAIN_URL + 'entity/discount'
URL_DEMAND = MAIN_URL + 'entity/demand/'
URL_PRODUCT = MAIN_URL + 'entity/product/'
URL_SERVICE = MAIN_URL + 'entity/service/'
URL_STORE = MAIN_URL + 'entity/store/'
URL_GET_PAYMENT_TEMPLATE = MAIN_URL + 'entity/paymentin/new'
URL_NEW_PAYMENT = MAIN_URL + 'entity/paymentin'


