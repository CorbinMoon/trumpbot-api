FROM python:3.7
COPY . /trumpbot-api
WORKDIR /trumpbot-api
RUN find ./bin -name "*.sh" -exec chmod +x {} \;
RUN ./bin/install_tensorflow.sh
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["./bin/start.sh"]