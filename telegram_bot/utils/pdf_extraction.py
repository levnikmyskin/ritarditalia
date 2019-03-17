import re
import fitz
from telegram_bot.utils.structs import Train
from telegram_bot.utils.trains_api import find_train_original_depart_station
from datetime import datetime


# Regex pattern to extract info from the PDF text
train_info_pattern = re.compile(r"Stazione di Partenza[\n\s]*(?P<depart_stat>[\w\s\.\-]+)Ore\s*(?P<depart_date>\d{2}:\d{2}\s-\s\d{2}/\d{2}/\d{4}).+Treno:\s*[A-Za-z\s]+(?P<code>\d+)(.+Carrozza:\s*(?P<coach>\d+)\nPosti:\s*(?P<seat>\d+[A-Z]))?",
                                re.MULTILINE | re.DOTALL)


def extract_info_from_text(text: str, user: str) -> Train:
    train = None
    match = train_info_pattern.search(text)
    if match is not None:
        code = match.group("code")
        station = match.group("depart_stat")
        depart_date = match.group("depart_date")
        # We absolutely need to have this info, if we don't stop the parsing and return None
        if all((code, station, depart_date)):
            station = find_train_original_depart_station(code)[0]
            depart_date = datetime.strptime(depart_date, "%H:%M - %d/%m/%Y")
        else:
            return None
        train = Train(
            -1,
            code,
            station,
            depart_date,
            user,
            checked=0,
            check_daily=False,
            coach=match.group("coach"),
            seat=match.group("seat")
        )
    return train


def extract_info_from_pdf(doc: fitz.Document, user: str) -> [Train]:
    trains_list = list()
    for i in range(doc.pageCount):
        page = doc.loadPage(i)
        text = page.getText("text")
        train = extract_info_from_text(text, user)
        if train is not None:
            trains_list.append(train)
    return trains_list
