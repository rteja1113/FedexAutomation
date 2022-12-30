import xlrd
import logging
import datetime
import django
django.setup()
from database.models import DailyService

logging.basicConfig(level=logging.DEBUG)


# print("The number of worksheets is {0}".format(book.nsheets))
# print("Worksheet name(s): {0}".format(book.sheet_names()))
# sh = book.sheet_by_index(0)
# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))    date

# # sh.cell_value(rowx=29, colx=3)))sh.cell()


def load_and_save_xls_file_to_db(file_path="../datasets/daily service worksheet-1216.xls"):
    # try
    DailyService.from_xls_file(file_path)
    # except Exception as e:
    # logging.error("Trying to insert Duplicate records !")


def save_file_to_db():
    pass


if __name__ == "__main__":
    load_and_save_xls_file_to_db()
    # load_xls_file()