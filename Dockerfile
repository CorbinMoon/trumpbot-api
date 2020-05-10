FROM python:3.7
RUN git clone --branch master https://github.com/CorbinMoon/trumpbot-sys-api.git
WORKDIR /trumpbot-sys-api
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["/trumpbot/api.py"]