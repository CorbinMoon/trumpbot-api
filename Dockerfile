FROM tensorflow/tensorflow:latest-py3
RUN git clone --branch master https://github.com/CorbinMoon/trumpbot-api.git
WORKDIR /trumpbot-api
RUN pip install -r requirements.txt
RUN chmod +x ./bin/start.sh
EXPOSE 80
ENTRYPOINT ["./bin/start.sh"]