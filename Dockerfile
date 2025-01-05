FROM python:3.12

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN python -m pip install Pillow

RUN apt-get update && apt-get install -y postgresql-client

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash usr && chmod 777 /opt /run

WORKDIR /usr

RUN mkdir /usr/static && mkdir /usr/media && chown -R usr:usr /usr && chmod 755 /usr

COPY --chown=usr:usr . .

RUN pip install -r requirements.txt

USER usr

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

