from datetime import datetime
from random import randint

from pytz import (
    timezone as Timezone,
)

from cores.settings import TIMEZONE


def generate_api_call_id() -> str:
    """
    Generate unique api call id
    """
    current_date = datetime.now().strftime("%m%d%Y_%H%M%S")

    random_num = randint(1, 10000000)
    invoice_code = "API_CALL_{}_{}".format(str(current_date), str(random_num))

    return invoice_code


def get_timezone(timezone: str = TIMEZONE) -> Timezone:
    """get timezone
    :timezone -> timezone input, default "Asia/Jakarta"
    """
    try:
        tz = Timezone(timezone)
        return tz
    except Exception:  # pragma: no cover
        return Timezone("Asia/Jakarta")
