FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /codes
COPY requirements /codes/
RUN pip install -r requirements/dev.txt
COPY . /code/
