from pony_data import *
import data_requests


with open('not_found.txt', 'w') as fil:
    pass


@db_session
def check_all_products():
    not_found_list = []
    products = select(prod.goods for prod in Rawsales_copy1)[:]
    print(f'Всего товаров: {len(products)}', type(products))
    # exit(0)

    for n, product in enumerate(products):
        if data_requests.get_product_meta_by_name(str(product).strip()):
            print(n, 'OK', product)
        else:
            not_found_list.append(product)
            print(n, 'НЕТ!', product)
            with open('not_found.txt', 'a') as fil:
                for i in not_found_list:
                    string = '--' + i + '--\n'
                    fil.write(string)


# print()
#     print(f'Не найдено {len(not_found_list)} товаров')
#     with open('not_found.txt', 'a') as fil:
#         for i in not_found_list:
#             string = '--' + i + '--\n'
#             fil.write(string)


check_all_products()