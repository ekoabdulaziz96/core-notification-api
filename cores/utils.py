from datetime import datetime, timedelta
from random import randint

from pytz import (
    timezone as Timezone,
    UTC,
)

from cores.settings import TIMEZONE, TIMEZONE_ADD_HOUR


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


def convert_datetime_to_aware_timezone(datetime: datetime, timezone: Timezone) -> datetime:
    """convert datetime obj saved in db to specific timezone
    :datetime -> datetime obj
    :timezone -> timezone obj
    """
    # dt_utc = datetime.replace(tzinfo=pytz.UTC)  # replace method --> aware UTC
    #  = dt_utc.astimezone(timezone)  # astimezone method --> convert to specific timezone
    dt_aware_timezone = (
        datetime - timedelta(hours=TIMEZONE_ADD_HOUR)
    ).replace(tzinfo=UTC).astimezone(timezone)

    return dt_aware_timezone
