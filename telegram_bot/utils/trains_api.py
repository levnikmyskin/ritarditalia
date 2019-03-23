import requests
import re
import pytz
from datetime import datetime
from telegram_bot.utils.db_utils import get_trains_to_monitor


def find_train_original_depart_station(train_code: str) -> [str]:
    endpoint = f"http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/{train_code}"
    req = requests.get(endpoint)
    if req.status_code == 200:
        p = re.compile(r'\d+\s-\s(?P<station_name>.+)\|\d+-(?P<station_code>\w+\d+)', re.MULTILINE)
        return p.findall(req.text)
    return list()


def get_train_status(station_code: str, train_code: str) -> dict:
    endpoint = f"http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/{station_code}/{train_code}"
    req = requests.get(endpoint)
    if req.status_code == 200:
        return req.json()
    return {'error': {'code': req.status_code, 'message': req.text}}


def timestamp_to_italy_datetime(timestamp: int) -> datetime:
    """
    Takes a Trenitalia timezone and convert it to a datetime object
    using the pytz timezone Europe/Rome
    :param timestamp: the Trenitalia timestamp
    :return: a datetime object with timezone Europe/Rome
    """
    tz = pytz.timezone('Europe/Rome')
    return datetime.fromtimestamp(timestamp / 1000, tz)


if __name__ == "__main__":
    to_mon = get_trains_to_monitor()
    print(to_mon)
