# Deveria ser o slim, mas está ocorrendo erro com o psygopg2
#FROM python:3.9.13-slim

FROM python:3.9.13

WORKDIR /user_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

#CMD [ "pytest", "tests/security_tests.py" ]
#CMD [ "pytest", "tests/webservice_tests.py" ]
CMD [ "python", "main.py" ]
