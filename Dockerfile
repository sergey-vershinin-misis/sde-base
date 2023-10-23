FROM python:3.11

RUN pip install fastapi
RUN pip install uvicorn

COPY ./ ./

EXPOSE 8000:8000

CMD ["python3", "main.py"]
