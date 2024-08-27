import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")  # set relative path

from models.emails import UserRecipient  # noqa
from seeders._parents import ParentSeeder  # noqa

# ----------------------------------------------------- PREPARE SEED DATA
PAYLOAD_USER_RECIPIENT_LIST = [
    dict(
        email="azizeko29undip@gmail.com",
    ),
    dict(
        email="ekoabdulaziz96@gmail.com",
    ),
]

# ----------------------------------------------------- CLASS SEEDER
class SeedUserRecipient(ParentSeeder):
    def process(self):
        try:
            for payload in PAYLOAD_USER_RECIPIENT_LIST:
                filter_data = {"email": payload["email"]}
                self._seed_table_with_one_filter(UserRecipient, filter_data, payload)

        except Exception as err:
            print(f"|ERROR|-{err}")


# -------------------------------------------------------run script
if __name__ == "__main__":
    SeedUserRecipient().process()
