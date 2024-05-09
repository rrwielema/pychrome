import random
from typing import List, Union

import requests
import pandas as pd
import os
import bs4 as bs
import httpagentparser
import sqlite3

from .common import USER_AGENT_DB


class UserAgentManager:
    def __init__(self, **kwargs):
        self.filters = kwargs
        self._agents = []

        if self.db_is_outdated():
            self.collect()
        if not kwargs.get('limit') or kwargs.get('limit') == 1:
            self._agents.append(UserAgent.from_db(**kwargs))
        else:
            self._agents.extend(UserAgent.from_db(**kwargs))

    @staticmethod
    def db_is_outdated() -> bool:
        modified = os.path.getmtime(USER_AGENT_DB)
        return pd.Timestamp.fromtimestamp(modified) < pd.Timestamp.now() - pd.Timedelta(days=30)

    @staticmethod
    def collect():
        r = requests.get('https://deviceatlas.com/blog/list-of-user-agent-strings')
        soup = bs.BeautifulSoup(r.content, 'lxml')
        all_user_agents_strings = soup.select('tr > td')
        user_agents = [UserAgent(ua.text.strip()) for ua in all_user_agents_strings]
        for ua in user_agents:
            ua.to_db()

    def __str__(self) -> str:
        num = random.randint(0, len(self._agents) - 1)
        return self._agents[num].string

    def __repr__(self) -> str:
        return self.__str__()


class UserAgent:
    def __init__(self, string: str):
        self.string = string

        data = httpagentparser.detect(string)
        self.platform_name = data.get('platform', {}).get('name')
        self.platform_version = data.get('platform', {}).get('version')
        self.os = data.get('os', {}).get('name')
        self.is_bot = data.get('bot', False)
        self.dist_name = data.get('dist', {}).get('name')
        self.dist_version = data.get('dist', {}).get('version')
        self.browser_name = data.get('browser', {}).get('name')
        self.browser_version = data.get('browser', {}).get('version')

    def as_df(self) -> pd.DataFrame:
        return pd.DataFrame([self.__dict__])

    def to_db(self):
        with sqlite3.connect(USER_AGENT_DB) as con:
            self.as_df().to_sql('ua', con, if_exists='append', index=False)

    @classmethod
    def from_db(cls, limit: int = 1, **kwargs) -> Union['UserAgent', List['UserAgent']]:
        with sqlite3.connect(USER_AGENT_DB) as con:
            df = pd.read_sql('select * from ua', con)
        for k, v in kwargs.items():
            df = df[df[k] == v]
        if limit > 1:
            return [cls(row.get('string')) for row in df.to_dict('records')]
        string = df.sample(1).string.iloc[0]
        return cls(string)

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return self.string
