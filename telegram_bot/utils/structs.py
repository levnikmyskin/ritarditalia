from collections import namedtuple


Train = namedtuple(
    'Train',
    ['id', 'code', 'depart_stat', 'depart_date', 'user', 'checked', 'check_daily', 'check_interval', 'coach', 'seat'],
    defaults=[0, False, None, None, None]
)
Station = namedtuple('Station', ['name', 'code'])
User = namedtuple('User', ['id', 'chat_id', 'name', 'email', 'lang', 'notification_via'])
