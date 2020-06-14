FROM python:3.7
RUN git clone --branch master https://github.com/CorbinMoon/trumpbot-api.git
WORKDIR /trumpbot-api
RUN chmod +x ./start.sh
EXPOSE 80
ENTRYPOINT ["./start.sh"]