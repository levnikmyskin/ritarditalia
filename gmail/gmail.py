from __future__ import print_function
import re
import pickle
import os.path
import base64
import MySQLdb
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from telegram_bot.utils.trains_api import find_train_original_depart_station
from telegram_bot.utils.structs import Train
from telegram_bot.utils.db_utils import create_user_from_row, has_mail_been_parsed, insert_train_in_db
from config import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def extract_info(message: bytes) -> re.Match:
    """
    Extract train id, departure date, departure station name and departure hours from an HTML message (byte encoded).
    :returns the result of the re module `search` method on the message. If there's a match, you will have the following
    groups: <ul><li>id: train id;</li><li>depart_date: departure date formatted as dd/mm/yyyy</li><li>depart_stat:
    departure station name (eg. Roma Termini)</li><li>hours: scheduled hours of train departure, formatted as hh:mm</li>
    """
    message = re.sub(r'(<.+?>)|[\r\t]', '', message.decode('utf-8'))  # Remove HTML tags and \r or \t

    # Virgin mother of God, this regex freaks me out the more I look at it.
    # Good thing is, it actually matches what we need
    p = re.compile(
        r'Treno.+?(?P<id>\d+).+?(?P<depart_date>\d{2}/\d{2}/\d{4}).+Partenza.+?(?P<depart_stat>[\w\s]+).+?(?P<hours>\d{2}:\d{2})',
        re.MULTILINE | re.DOTALL
    )
    return p.search(message)


def fetch_mails(user_email: str, conn: MySQLdb.Connection) -> [dict]:
    """
    Calls Google Gmail API on the user_email in order to retrieve his Trenitalia emails.
    :param user_email: the user email
    :param conn: MySQLdb.Connection instance
    :return: a list of dictionaries containing all appropriate emails retrieved.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                'credentials.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
            print(f"Clicca n po': {auth_url}")
            code = input("Mettilo tutto: ")
            flow.fetch_token(code=code)
            creds = flow.credentials
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    messages_list = list()
    after = datetime.now(tz=pytz.timezone('Europe/Rome')) - timedelta(minutes=30)
    results = service.users().messages().list(
        userId=user_email,
        q=f'from:"Trenitalia" after:{int(after.timestamp())}'
    ).execute()
    for message in results['messages']:
        if not has_mail_been_parsed(message['id'], conn):
            messages_list.append(service.users().messages().get(userId=user_email, id=message['id']).execute())
    return messages_list


def parse_emails(mails: [dict], user_id: int, conn: MySQLdb.Connection):
    for mail in mails:
        info = extract_info(base64.urlsafe_b64decode(mail['payload']['parts'][0]['body']['data']))
        if info is not None:
            # We retrieve the original departure station, we always take the first one in this case
            # TODO warn user about it
            original_station = find_train_original_depart_station(info.group('id'))
            train_date = datetime.strptime(f"{info.group('depart_date')} {info.group('hours')}", "%d/%m/%Y %H:%M")
            insert_train_in_db(
                Train(code=info.group('id'), depart_date=train_date, depart_stat=original_station[0]),
                conn
            )
        else:
            print(f"Couldn't extract info for email: {mail}")


def main():
    conn = MySQLdb.connect(passwd=DB_PASSWORD, user=DB_USER, host=DB_HOST, db=DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, chat_id, name, email FROM users")
    for user in cursor:
        usr = create_user_from_row(user)
        mails = fetch_mails(usr.email, conn)
        parse_emails(mails, usr.id, conn)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
