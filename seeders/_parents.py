import os
import random
import string
import sys

from server import app

""" set relative path """
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")


class ParentSeeder(object):
    def __init__(self):
        self.app = app
        self.app.debug = True
        self.app.app_context().push()

    @classmethod
    def _generate_random_string(cls, length: int):
        return "".join(random.choice(string.ascii_lowercase) for i in range(length))

    def _seed_table_with_one_filter(self, ORM_class: object, filter_data: dict, payload: dict) -> object:
        """create dummy data for table, using procedure get or create
        :ORM_class -> ORM class that relate a table in DB
        :filter_data -> filter data for exist or not in DB
        :payload -> payload data to be added
        """
        data_record = ORM_class.query.filter_by(**filter_data).first()

        if not data_record:
            payload = payload

            data_record = ORM_class(**payload)
            data_record.save()
            print(f"|SUCCES ADD NEW DATA|-{data_record}")
        else:
            print(f"|DATA EXIST|-{data_record}")

        return data_record

    def _seed_table_with_two_filter(
        self, ORM_class: object, filter_data1: dict, filter_data2: dict, payload: dict
    ) -> None:
        """create dummy data for table, using procedure get or create
        :ORM_class -> ORM class that relate a table in DB
        :filter_data1 -> filter data for exist or not in DB
        :filter_data2 -> filter data for exist or not in DB
          -> using AND logic for filter_data1 AND filter_data2 in where clause
        :payload -> payload data to be added
        """
        data_record = ORM_class.query.filter_by(**filter_data1).filter_by(**filter_data2).first()

        if not data_record:
            payload = payload

            data_record = ORM_class(**payload)
            data_record.save()
            print(f"|SUCCES ADD NEW DATA|-{data_record}")
        else:
            print(f"|DATA EXIST|-{data_record}")
