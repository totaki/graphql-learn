import datetime as dt
import calendar


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

