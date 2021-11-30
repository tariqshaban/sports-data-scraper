import datetime
import time


class DateTimeHandler:
    """
    Set of static methods that aid some time manipulations.

    Attributes
    ----------

    Methods
    -------
        datetime_from_utc_to_local(utc):
            Converts UTC time standard to Local time standard.
        get_dates_between(start_date=datetime.date.today() - datetime.timedelta(days=7),
                              end_date=datetime.date.today()):
            Gets dates between two dates in YYYYmmDD format.
    """

    @staticmethod
    def datetime_from_utc_to_local(utc):
        """
        Converts UTC time standard to Local time standard.

        :param datetime.date utc: Specify the utc time
        :return: DateTime in local timing
        """

        epoch = time.mktime(utc.timetuple())
        offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
        return utc + offset

    @staticmethod
    def get_dates_between(start_date=datetime.date.today() - datetime.timedelta(days=7),
                          end_date=datetime.date.today()):
        """
        Gets dates between two dates in YYYYmmDD format.

        :param datetime.date start_date: Specify the start date of the search
        :param datetime.date end_date: Specify the end date of the search
        :return: An array of dates as str
        """

        if start_date > end_date:
            raise ValueError('start_date cannot be less than end_date')

        days_between = []

        delta = end_date - start_date

        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            days_between.append(day.strftime('%Y%m%d'))

        return days_between
