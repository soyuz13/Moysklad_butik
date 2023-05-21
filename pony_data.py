from pony.orm import *
from datetime import datetime
from config import *

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


db.bind(provider='mysql', host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_BASE, port=DB_PORT)

db.generate_mapping(create_tables=True)
