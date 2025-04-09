FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /usr/src/QA_Hub

COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY ./QA_Hub /usr/src/QA_Hub

EXPOSE 8000
ENTRYPOINT ["bash", "-c", "exec \"$@\"", "--"]