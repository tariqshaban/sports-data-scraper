import datetime


class DateTimeHandler:
    """
    Set of static methods that aid some time manipulations.

    Attributes
    ----------

    Methods
    -------
        get_dates_between(start_date=datetime.date.today() - datetime.timedelta(days=7),
                              end_date=datetime.date.today()):
            Gets dates between two dates in YYYYmmDD format.
        year_month_day_to_date(date):
            Gets dates between two dates in YYYYmmDD format.
    """

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

    @staticmethod
    def year_month_day_to_date(date):
        """
        Converts date string in %Y%m%d format into a date object

        :param str date: Specify the date as a string in %Y%m%d format (20211001)
        :return: An date object
        """

        return datetime.datetime.strptime(date, '%Y%m%d')
