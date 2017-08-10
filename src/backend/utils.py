import datetime as dt
import calendar
from enums import TaskStatus

def get_datetime(datetime=None, offset=0):
    if not datetime:
        datetime = dt.datetime.utcnow()
    delta = calendar.weekday(datetime.year, datetime.month, datetime.day)
    _ = datetime - dt.timedelta(days=delta) + dt.timedelta(days=offset * 7)
    return dt.datetime(_.year, _.month, _.day)


def get_iteration_datetime(args):
    return get_datetime(
        datetime=args.get('date', None),
        offset=args.get('offset', None)
    )


def get_directions(next, prev):
    from_backlog = (next == TaskStatus.TODO and prev == TaskStatus.BACKLOG)
    to_backlog = (next == TaskStatus.BACKLOG and prev == TaskStatus.TODO)
    return from_backlog, to_backlog


def get_args_by_list(args, list_keys):
    return [args.get(key, None) for key in list_keys]


