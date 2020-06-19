FROM python:3.7
COPY . /trumpbot-api
WORKDIR /trumpbot-api
RUN chmod +x ./bin/install_tensorflow.sh
RUN chmod +x ./bin/start.sh
RUN echo "y y y y y y y" | ./bin/install_tensorflow.sh
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["./bin/start.sh"]