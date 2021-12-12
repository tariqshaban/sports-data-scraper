import datetime


class ProgressHandler:
    """
    Set of static methods that aid some progress manipulations.

    Attributes
    ----------
        __last_accessed     Last time show_progress method has been called.
        __remaining_time    Stores remaining time in a formatted string

    Methods
    -------
        show_progress(elapsed=0, total=100):
            Shows scraping progress in a formatted manner.
        reset_progress():
            Nullifies the attributes in order to receive new progress.
    """

    __last_accessed = None
    __remaining_time = None

    @staticmethod
    def show_progress(elapsed=0, total=100):
        """
        Shows scraping progress in a formatted manner.

        :param int elapsed: Specify the elapsed retrieved pages
        :param int total: Specify the total number of pages
        :return: A string denoting the progress
        """

        if ProgressHandler.__last_accessed is None:
            ProgressHandler.__last_accessed = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
            ProgressHandler.__remaining_time = total * 0.9  # Assumes 900 milliseconds for each web request
        else:
            elapsed_time = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds() \
                           - ProgressHandler.__last_accessed
            all_time_for_downloading = (elapsed_time * total / elapsed)
            ProgressHandler.__remaining_time = all_time_for_downloading - elapsed_time

        if not isinstance(elapsed, int):
            raise ValueError('elapsed must be an integer')

        if not isinstance(total, int):
            raise ValueError('total must be an integer')

        if elapsed > total:
            raise ValueError('elapsed cannot be greater than total')

        return f'{elapsed}/{total}\t\t' \
               f'{"{:.2f}".format(round(elapsed / total * 100, 2))}%\t\t' \
               f'ETA: {"{:.2f}".format(round(ProgressHandler.__remaining_time, 2))} second(s)'

    @staticmethod
    def reset_progress():
        """
        Nullifies the attributes in order to receive new progress.
        """

        ProgressHandler.__last_accessed = None
        ProgressHandler.__remaining_time = None
