FROM python:stretch
RUN apt update && apt upgrade -y && apt install -y build-essential libmariadbclient-dev && \
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib requests mysqlclient \
python-telegram-bot pytz
