FROM python:3.7

COPY requirements.txt /requirements.txt

RUN pip install --requirement /requirements.txt

COPY src /src

EXPOSE 80

ENTRYPOINT ["/src/entrypoint"]

