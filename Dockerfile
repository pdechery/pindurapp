FROM python:3.11

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
  && chown python:python -R /app

USER python

ENV PYTHONUNBUFFERED="true" \
  PYTHONPATH="." \
  PATH="${PATH}:/home/python/.local/bin" \
  USER="python"

COPY --chown=python:python requirements.txt .
COPY --chown=python:python instance instance
COPY --chown=python:python pindurapp pindurapp


RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD gunicorn -w 2 pindurapp:app --bind 0.0.0.0