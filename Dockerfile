FROM python:3.11

WORKDIR /fastapi

COPY ./requirements.txt /fastapi/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi/requirements.txt

COPY . /fastapi

EXPOSE 8000

CMD ["uvicorn", "main:app", "--proxy-headers", "--reload","--host", "0.0.0.0", "--port", "8000"]