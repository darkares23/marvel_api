# pull official base image
FROM python:3.10 as development_build

# set work directory
WORKDIR /marvel
COPY pyproject.toml poetry.lock ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
# RUN poetry install -n --no-ansi
RUN poetry lock --check && PIP_IGNORE_INSTALLED=1 PIP_USER=1 poetry install

# copy project
COPY . /marvel/