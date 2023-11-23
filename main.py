from fastapi import FastAPI, Query, Path
from vacancies.vacancies_set import VacanciesSet, VacanciesInfo, VacanciesCount, GroupingType

app = FastAPI()


@app.get("/")
async def root():
    """
    Возвращает Ok, если сервер запущен и API функционирует
    """
    return 'Ok'


@app.get("/vacancies/info/{query}", response_model=VacanciesInfo)
async def info(query: str = Path(description="Фильтр, используемый для поиска вакансий")) -> VacanciesInfo:
    """
    С помощью открытого API HeadHunter выполняет поиск вакансий по заданному фильтру query за предыдущий месяц и
    возвращает основные параметры найденного набора: количество и средние значения границ зарплатной вилки в них.
    Запрашиваемое количество вакансий - не более 100.
    """
    return VacanciesSet(query).get_info()


@app.get("/vacancies/count/{query}", response_model=VacanciesCount)
async def count(
        query: str = Path(description="Фильтр, используемый для поиска вакансий"),
        group_by: GroupingType = Query(default=GroupingType.by_employer, description="Способ группировки вакансий")
) -> VacanciesCount:
    """
    С помощью открытого API HeadHunter выполняет поиск вакансий по заданному фильтру query за предыдущий месяц,
    группирует их по работодателю, по виду занятости или по необходимому для работы опыту и возвращает топ 5 групп с
    указанием для каждой работодателя, вида занятости или опыта работы и количества вакансий в ней.
    Запрашиваемое количество вакансий - не более 100.
    """
    return VacanciesSet(query).get_count_by(group_by)

