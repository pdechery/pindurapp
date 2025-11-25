FROM python:3.9-slim

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
COPY --chown=python:python app app
COPY --chown=python:python instance instance

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Set the command to run the Flask application
CMD [ "python3", "-m" , "flask", "--app", "app", "run", "--host=0.0.0.0"]