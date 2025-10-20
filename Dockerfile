FROM python:3.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir --upgrade uvicorn

COPY . /code/app

ENV PYTHONPATH=/code/app

EXPOSE 80

CMD ["uvicorn", "app.handler:app", "--host", "0.0.0.0", "--port", "80"]
