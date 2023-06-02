FROM python:3.11

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales

RUN useradd -rms /bin/bash user_pb && chmod 777 /opt/run

WORKDIR /user_pb

RUN mkdir /user_pb/static && mkdir /user_pb/media && chown -R user_pb:user_pb /user_pb && chmod 755 /user_pb

COPY --chown=user_pb:user_pb . .

RUN pip install -r requirements.txt

USER user_pb

CMD ["gunicorn, '-b", "0.0.0.0:8000", "personal_blog.wsgi:application"]
