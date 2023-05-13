from pony.orm import *
from datetime import datetime

db = Database()


class Rawsales_copy1(db.Entity):
    field0 = Optional(int)
    sale_id = Optional(int)
    goods = Optional(str)
    fullPrice = Optional(float)
    count = Optional(int)
    discValue = Optional(float)


class All_checks(db.Entity):
    dtime = Optional(datetime)
    id = PrimaryKey(int)
    checksum = float
    card = Optional(int)
    discvalue = Optional(float)


db.bind(provider='mysql', host='95.154.87.128', user='discount', passwd='Vl@zer52@7$', db='vlazer', port=33306)

db.generate_mapping(create_tables=True)
