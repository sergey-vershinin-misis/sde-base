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
    С помощью открытого API HeadHunter выполняет поиск вакансий по заданному фильтру query и возвращает основные
    параметры найденного набора: количество и средние значения границ зарплатной вилки в них
    """
    return VacanciesSet(query).get_info()


@app.get("/vacancies/count/{query}", response_model=VacanciesCount)
async def count(
        query: str = Path(description="Фильтр, используемый для поиска вакансий"),
        group_by: GroupingType = Query(default=GroupingType.by_employer, description="Способ группировки вакансий")
) -> VacanciesCount:
    """
    С помощью открытого API HeadHunter выполняет поиск вакансий по заданному фильтру query, группирует их по
    работодателю и для каждой группы возвращает наименование работодателя и количество найденных вакансий от него
    """
    return VacanciesSet(query).get_count_by(group_by)

