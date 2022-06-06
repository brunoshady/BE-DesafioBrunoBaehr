FROM python:3.9.13

WORKDIR /order_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

#CMD [ "pytest", "tests/webservice_tests.py" ]
CMD [ "python", "main.py" ]