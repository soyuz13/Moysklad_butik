from datamodel import Demand, PaymentInTemplate, Operations, Operation, Position, Store, Assortment, AllOrganizations, Organization, AllStores, Product, Products, AllDiscounts, Discount, NewClientDiscounts, Disc, DiscountContragent, AllContragents, Contragent
import requests
from requests.auth import HTTPBasicAuth
from config import *
import pprint
import datetime as ddt
from pony_data import *
import urllib.parse


def get_organization_meta(name: str='vasily_t1000'):
    res = requests.get(URL_ORGANIZATION, auth=HTTPBasicAuth(USER, PASS))
    org = AllOrganizations(**res.json())
    for i in org.rows:
        if i.name == name:
            return i.meta


def get_mainstore_meta(name: str='Основной склад'):
    res = requests.get(URL_STORE, auth=HTTPBasicAuth(USER, PASS))
    store = AllStores(**res.json())
    for i in store.rows:
        if i.name == name:
            return i.meta


ORG_META = get_organization_meta()
STORE_META = get_mainstore_meta()


def get_discount_meta(name: str='НС1'):
    res = requests.get(URL_DISCOUNT, auth=HTTPBasicAuth(USER, PASS))
    disc = AllDiscounts(**res.json())
    for i in disc.rows:
        if i.name == name:
            return i.meta


# def get_all_contragents():
#     res = requests.get(URL_CONTRAGENT, auth=HTTPBasicAuth(USER, PASS))
#     cont = AllContragents(**res.json())
#
#     for n, i in enumerate(cont.rows):
#         print(n, i.name, i.phone, i.id)


# def get_contragent_meta(id: str):
#     res = requests.get(URL_CONTRAGENT + id, auth=HTTPBasicAuth(USER, PASS))
#     cont = Contragent(**res.json())
#     print(cont.name, cont.phone, cont.discounts[0].demand_sum_correction)
#     return cont.meta


# def create_contragent():
#     new_cont = Contragent()
#     new_cont.name = 'Самый тестовый'
#     new_cont.phone = '89020531011'
#     new_cont.created = '2021-09-18 16:55:55'
#     new_cont.tags = ['розничный клиент']
#     new_cont.company_type = 'individual'
#     new_cont.discounts = [DiscountContragent(discount=Disc(meta=get_discount_meta()), demandSumCorrection=1234000.00)]
#
#     json_ = new_cont.dict(by_alias=True, exclude_defaults=True)
#     res = requests.post(URL_CONTRAGENT, auth=HTTPBasicAuth(USER, PASS), json=json_)
#     pprint.pprint(res.json())


def get_product_meta_by_name(name):
    data = {'filter': f'name={name}'}
    print(data)
    url = URL_PRODUCT + f'?{urllib.parse.urlencode(data)}'
    res = requests.get(url, auth=HTTPBasicAuth(USER, PASS))
    prod = Products(**res.json())
    # print('Ответ: ', prod.rows)

    if prod.rows:
        return prod.rows[0].meta
    else:
        print(f'Товар "{name}" не найден!')


def get_contragent_meta_by_card(card):
    url = URL_CONTRAGENT + f'?filter=discountCardNumber={card}'
    res = requests.get(url, auth=HTTPBasicAuth(USER, PASS))
    cont = Products(**res.json())

    if cont.rows:
        return cont.rows[0].meta
    else:
        print(f'Покупатель с картой {card} не найден!')


def create_demand(moment: str, contragent_meta, positions, name):
    new_demand = Demand(organization=Organization(meta=ORG_META),
                        agent = Contragent(meta=contragent_meta),
                        store = Store(meta=STORE_META),
                        vatEnabled=False,
                        vatIncluded=False,
                        moment=moment,  # дата отгрузки = дате чека
                        name=name,      # номер отгрузки = номеру чека
                        positions=positions)

# new_demand = Demand(organization=Organization(meta=get_organization_meta()),
    #                     agent = Contragent(meta=get_contragent_meta('5df78613-e977-11ed-0a80-110f00498dbc')),
    #                     store = Store(meta=get_mainstore_meta()),
    #                     vatEnabled=False,
    #                     vatIncluded=False,
    #                     moment=moment)
    # new_demand.positions = [Position(quantity=20,
    #                                  price=3500,
    #                                  assortment=Assortment(meta=get_good_meta_by_name('КР Айришкрим')))]

    # создаем отгрузку
    res = requests.post(URL_DEMAND, json=new_demand.dict(by_alias=True, exclude_none=True), auth=HTTPBasicAuth(USER, PASS))

    # получаем мета созданной отгрузки, добавляем их в список операций для получения шаблона входящего платежа
    demand_meta = res.json()['meta']
    ops = Operations()
    op1 = Operation()
    op1.meta = demand_meta
    ops.operations = [op1]

    # запрос шаблона входящего платежа на основании отгрузки
    res = requests.put(URL_GET_PAYMENT_TEMPLATE, json=ops.dict(by_alias=True, exclude_none=True), auth=HTTPBasicAuth(USER, PASS))

    payment_template = PaymentInTemplate(**res.json())
    payment_template.moment = moment    # дата платежа = дате чека
    payment_template.name = str(name)   # номер платежа = номеру чека

    # создаем входящий платеж
    res = requests.post(URL_NEW_PAYMENT, json=payment_template.dict(by_alias=True, exclude_none=True), auth=HTTPBasicAuth(USER, PASS))


@db_session
def get_products_by_saleid(sale_id: int) -> list:
    products = select(prod for prod in Rawsales_copy1 if prod.sale_id == sale_id)[:]
    return products


def get_product_list(sale_id: int) -> list:
    meta_prod_list = []
    product_list = get_products_by_saleid(sale_id)
    print(f'Чек: {sale_id}, товаров: {len(product_list)}')

    for n, j in enumerate(product_list):
        print(n+1, j.goods)
        product_meta = get_product_meta_by_name(j.goods)
        meta_prod_list.append(Position(quantity=j.count,
                                       price=j.fullPrice*100,
                                       discount=j.discValue,
                                       assortment=Assortment(meta=product_meta)
                                       ))
    # print(meta_prod_list)
    print()
    return meta_prod_list


@db_session
def get_all_cheks(date1: ddt.date=ddt.date(2017, 12, 15),
                  date2: ddt.date=ddt.date(2017, 12, 15)):
    '''запрос в базе всех уникальных чеков за промежуток времени'''
    cheks = select(q for q in All_checks if date1 <= q.dtime.date() <= date2)[:]
    return cheks


def main():
    check_list = get_all_cheks()
    check_list = check_list[:1]

    # по каждому чеку
    for check in check_list:
        positions = get_product_list(check.id)
        contragent = get_contragent_meta_by_card(check.card) if get_contragent_meta_by_card(check.card) else get_contragent_meta_by_card(999)
        moment = datetime.strftime(check.dtime + ddt.timedelta(hours=14), '%Y-%m-%d %H:%M:%S')
        name = check.id
        create_demand(moment, contragent, positions, name)


if __name__ == '__main__':
    main()