FROM python:3.12.0-slim

# Dependencies for psycopg2
RUN apt update && apt install -y libpq-dev gcc

COPY sreality sreality
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

ENV FLASK_APP=sreality.server
ENV FLASK_RUN_HOST=0.0.0.0

COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]