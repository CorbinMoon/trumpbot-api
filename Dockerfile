FROM python:3.7
RUN git clone --branch v1.15.0 https://github.com/tensorflow/tensorflow --single-branch
RUN chmod +x ./tensorflow/configure && ./tensorflow/configure
COPY . /trumpbot-api
WORKDIR /trumpbot-api
RUN pip install -r requirements.txt
RUN chmod +x ./bin/start.sh
EXPOSE 80
ENTRYPOINT ["./bin/start.sh"]