import csv
import re
from datetime import datetime

from pymongo import MongoClient


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        list_row = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = dict(row)
            row['Цена'] = int(row['Цена'])
            row['Дата'] += '.2019'
            row['Дата'] = datetime.strptime(row['Дата'], '%d.%m.%Y')
            list_row.append(row)
        db.insert_many(list_row)


def find_cheapest(db):
    """
    Найти самые дешевые билеты
    Документация: https://docs.mongodb.com/manual/reference/operator/aggregation/sort/
    """
    return list(db.find().sort("Цена", 1))


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и выведите их по возрастанию цены
    """
    name = re.escape(name)
    regex = re.compile(name)
    return list(db.find({'Исполнитель': regex}).sort("Цена", 1))


def find_by_date(date_1, date_2, db):
    date_1 = datetime_convert(date_1)
    date_2 = datetime_convert(date_2)
    return list(db.find({'Дата': {'$gt': date_1, '$lt': date_2}}))


def datetime_convert(date):
    return datetime.strptime(date, '%d.%m.%Y')


if __name__ == '__main__':
    client = MongoClient()
    mydb = client.homework
    mydb_ticket = mydb.ticket
    # read_data('artists.csv', mydb_ticket)
    # print(find_cheapest(mydb_ticket))
    # print(find_by_name('в', mydb_ticket))
    print(find_by_date("21.3.2019", "24.10.2019", mydb_ticket))
