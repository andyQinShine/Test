from app.base.envBase import EnvBase
from itertools import count
from collections import defaultdict, deque
from functools import partial

import arrow

class CleanerBase(EnvBase):
    cleaner_count = count(1)

    def __init__(self, rolling_window, buffer_day):
        self.name = f"{self.__class__.name}_ {next(self.cleaner_count)}"
        self.env.cleaners.update({self.name : self})
        self.rolling_window = rolling_window
        self.buffer_day = buffer_day
        self.data = None

    @property
    def startdate(self):
        date = arrow.get(self.env.fromdate).shift(days=-self.buffer_day)

        return date.format('YYYY-MM-DD HH:mm:ss')

    def init_data(self):
        self.data = defaultdict(partial(deque, maxlen = self.rolling_window))

        for key, value in self.env.readers.items():
            buffer_data = value.load(fromdate=self.startdate, todate=self.env.fromdate)
            self.data[key].extend((i['close'] for i in buffer_data))


