import datetime


class ProgressHandler:
    __last_accessed = None
    __remaining_time = None

    @staticmethod
    def show_progress(elapsed=0, total=100):
        """
        Shows scraping progress in a formatted manner

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

        return f'{elapsed}/{total} ' \
               f'({round(elapsed / total * 100, 2)}%, ' \
               f'ETA:{round(ProgressHandler.__remaining_time, 2)})'
