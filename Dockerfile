FROM python:3.7
RUN git clone --branch master https://github.com/CorbinMoon/trumpbot-api.git
WORKDIR /trumpbot-api
RUN pip install -r requirements.txt
# run unit tests
# RUN python -m unittest discover -s test
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["api.py"]