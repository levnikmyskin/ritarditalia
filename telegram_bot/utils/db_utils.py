import MySQLdb

from telegram_bot.utils.structs import User, Station, Train
from telegram_bot.utils.exceptions import TrainInPastError
from datetime import datetime, timedelta
from config import *


def get_user(conn: MySQLdb.Connection, user_id="", chat_id="") -> User:
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    else:
        cursor.execute("SELECT * FROM users WHERE chat_id=%s", (chat_id,))
    row = cursor.fetchone()
    if not row:
        return None
    user = create_user_from_row(row)
    cursor.close()
    return user


def create_user_from_row(row) -> User:
    return User(row[0], row[1], row[2], row[3], row[4], row[5])


def get_or_save_user(chat_id: str, username: str, email: str, notification_via: str, conn: MySQLdb.Connection):
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT id FROM users WHERE chat_id=%s) THEN "
                   "INSERT INTO users(chat_id, name, email, notification_via) VALUES(%s, %s, %s, %s);"
                   "END IF;",
                   (chat_id, chat_id, username, email, notification_via))
    conn.commit()
    return get_user(conn, chat_id=chat_id)


def update_user(user: User, conn: MySQLdb.Connection, commit=True):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=%s,email=%s,notification_via=%s,lang=%s WHERE chat_id=%s",
        (user.name, user.email, user.notification_via, user.lang),
    )
    if commit:
        conn.commit()
    cursor.close()


def update_user_lang(conn: MySQLdb.Connection, user_id="", chat_id="", lang="it", commit=True):
    cursor = conn.cursor()
    if user_id:
        cursor.execute("UPDATE users SET lang=%s WHERE id=%s", (lang, user_id))
    else:
        cursor.execute("UPDATE users SET lang=%s WHERE chat_id=%s", (lang, chat_id))

    if commit:
        conn.commit()
    cursor.close()


def get_station_from_code(station_code: str, conn: MySQLdb.Connection) -> Station:
    cursor = conn.cursor()
    cursor.execute("SELECT `name`, `code` FROM stations WHERE code=%s", (station_code,))
    row = cursor.fetchone()
    if not row:
        return None
    station = Station(name=row[0], code=row[1])
    cursor.close()
    return station


def has_mail_been_parsed(mail_id: str, conn: MySQLdb.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT from_mail_id FROM monitoring WHERE from_mail_id=%s)", (mail_id,))
    return bool(cursor.fetchone())


def insert_train_in_db(train: Train, conn: MySQLdb.Connection, commit=True):
    if train.depart_date >= datetime.now() or train.check_daily:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO monitoring (train, station, departDate, user, check_daily, check_interval, coach, seat) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
            (train.code, train.depart_stat, train.depart_date, train.user, train.check_daily, train.check_interval,
             train.coach, train.seat))
        if commit:
            conn.commit()
        cursor.close()
    else:
        raise TrainInPastError(f"Train depart date: {train.depart_date}; now: {datetime.now()}")


def get_all_trains(chat_id: str, conn: MySQLdb.Connection) -> [Train]:
    trains = list()
    cursor = conn.cursor()
    cursor.execute("SELECT id, train, station, departDate, user, checked, check_daily, check_interval, coach, seat "
                   "FROM monitoring WHERE user=%s", (chat_id,))
    for row in cursor:
        trains.append(Train(*row))
    cursor.close()
    return trains


def get_subset_of_trains(chat_id: str, start: int, conn: MySQLdb.Connection) -> [Train]:
    trains = list()
    cursor = conn.cursor()
    cursor.execute("SELECT id, train, station, departDate, user, checked, check_daily, check_interval, coach, seat "
                   "FROM monitoring "
                   "WHERE id >= %s AND user = %s LIMIT 7", (start, chat_id))
    for row in cursor:
        trains.append(Train(*row))
    cursor.close()
    return trains


def get_train(pk: int, conn: MySQLdb.Connection) -> Train:
    cursor = conn.cursor()
    cursor.execute("SELECT id, train, station, departDate, user, checked, check_daily, check_interval, coach, seat "
                   "FROM monitoring "
                   "WHERE id=%s", (pk,))
    row = cursor.fetchone()
    train = Train(*row)
    cursor.close()
    return train


def delete_train(pk: int, conn: MySQLdb.Connection):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM monitoring WHERE id=%s", (pk,))
    conn.commit()
    cursor.close()


def update_train_checked(pk: int, conn: MySQLdb.Connection):
    cursor = conn.cursor()
    cursor.execute("UPDATE monitoring set checked = checked + 1 WHERE id=%s", (pk,))
    conn.commit()
    cursor.close()


def connect_db() -> MySQLdb.Connection:
    return MySQLdb.Connect(passwd=DB_PASSWORD, user=DB_USER, host=DB_HOST, db=DB_NAME, use_unicode=True, charset="utf8mb4")


def get_trains_to_monitor(conn: MySQLdb.Connection) -> [Train]:
    train_lists = list()
    cursor = conn.cursor()

    max_date = datetime.now() + timedelta(hours=4)
    cursor.execute("SELECT id, train, station, departDate, user, checked, check_daily, check_interval, coach, seat "
                   "FROM monitoring WHERE (departDate BETWEEN %s AND %s"
                   "OR check_daily=TRUE)", (datetime.now(), max_date))
    for elems in cursor:
        train_lists.append(
            Train(*elems)
        )
    return train_lists


def search_stations(station_name: str) -> [Station]:
    conn = MySQLdb.connect(passwd=DB_PASSWORD, user=DB_USER, host=DB_HOST, db=DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT name, code FROM stations WHERE name LIKE "%%{station_name}%%"')
    stations = [Station(name=name, code=code) for name, code in cursor]
    cursor.close()
    conn.close()
    return stations


def store_feedback(feedback: str, chat_id: str, conn: MySQLdb.Connection):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedbacks(user, feedback) VALUES(%s, %s)",
                   (chat_id, feedback))
    conn.commit()
    cursor.close()