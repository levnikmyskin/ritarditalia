from collections import namedtuple
import enum


class TrainStatus(enum.Enum):
    AVAILABLE = enum.auto()
    ERROR = enum.auto()
    NOT_AVAILABLE = enum.auto()


class MonitorConversationStates(enum.Enum):
    STARTED = enum.auto()
    SEND_TRAIN_CODE = enum.auto()
    SEND_STATION = enum.auto()
    CONFIRM_TRAIN = enum.auto()
    SEND_DATE = enum.auto()
    SEND_HOURS = enum.auto()
    SEND_COACH_SEAT = enum.auto()
    CONFIRM_MONITORING = enum.auto()


Train = namedtuple(
    'Train',
    ['id', 'code', 'depart_stat', 'depart_date', 'user', 'checked', 'check_daily', 'check_interval', 'coach', 'seat'],
    defaults=[0, False, None, None, None]
)
Station = namedtuple('Station', ['name', 'code'])
User = namedtuple('User', ['id', 'chat_id', 'name', 'email', 'lang', 'notification_via'])
