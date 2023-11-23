from datetime import datetime, timedelta

import pandas as pd
import requests
from pydantic import BaseModel
from enum import Enum


HH_API_URL = 'https://api.hh.ru/vacancies'


class VacanciesInfo(BaseModel):
    """
    Основная информация о наборе вакансий: исходный запрос, количество найденных вакансий и средние
    значения нижней и верхней границ зарплатных вилок
    """
    query: str
    count: int
    salary_from: float
    salary_to: float


class VacanciesCountGroup(BaseModel):
    """наименование группы и количество вакансий в ней"""
    name: str
    count: int


class VacanciesCount(BaseModel):
    """Количество вакансий в группах, полученных при группировке набора вакансий по некоторому признаку"""
    query: str
    groups: list[VacanciesCountGroup]


class GroupingType(str, Enum):
    """Способы группировки найденных вакансий"""
    by_employer = "by_employer"
    by_experience = "by_experience"
    by_schedule = "by_schedule"


class VacanciesSet:
    def __init__(self, query):
        self.query = query
        self._load()

    def _load(self):
        v_page_json = self._get_vac_page_json()
        found_items = v_page_json['items']

        for i in range(1, v_page_json['pages']):
            found_items.extend(self._get_vac_page_json(i)['items'])

        self.data_frame = pd.json_normalize(found_items)

    def _get_vac_page_json(self, page_number: int = 0):

        current_date = datetime.today()
        start_date = current_date - timedelta(30)
        params = {
            'text': f'NAME:("{self.query}")',
            'area': 1,
            'date_from': start_date.strftime('%Y-%m-%d'),
            'date_to': current_date.strftime('%Y-%m-%d'),
            'per_page': 100,
            'page': page_number
        }

        with requests.get(HH_API_URL, params=params) as request:
            return request.json()

    def get_data(self):
        return self.data_frame

    def get_info(self) -> VacanciesInfo:
        return VacanciesInfo(query=self.query,
                             count=self.data_frame.shape[0],
                             salary_from=self.data_frame['salary.from'].mean(),
                             salary_to=self.data_frame['salary.to'].mean())

    def _get_count_by(self, group_column: str = 'employer.name', limit_to: int = 5) -> VacanciesCount:
        group_series = self.data_frame[group_column].value_counts()
        n = min(limit_to, group_series.shape[0])

        res = VacanciesCount(query=self.query, groups=[])
        for item in group_series[:n].items():
            res.groups.append(VacanciesCountGroup(name=item[0], count=item[1]))
        return res

    def get_count_by(self, grouping_type):
        if grouping_type == GroupingType.by_employer:
            return self._get_count_by()
        elif grouping_type == GroupingType.by_schedule:
            return self._get_count_by('schedule.name')
        else:
            return self._get_count_by('experience.name')

