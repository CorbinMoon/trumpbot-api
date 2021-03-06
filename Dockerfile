FROM python:3.7
COPY . /trumpbot-api
WORKDIR /trumpbot-api
RUN pip install -r requirements.txt
RUN chmod +x ./bin/start.sh
EXPOSE 80
ENTRYPOINT ["./bin/start.sh"]
