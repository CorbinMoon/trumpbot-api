FROM python:3.7
RUN git clone --branch master https://github.com/CorbinMoon/trumpbot-api.git
WORKDIR /trumpbot-api
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["/trumpbot/api.py"]