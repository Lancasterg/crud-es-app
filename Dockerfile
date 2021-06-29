FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install python3.8 python3.8-dev python3.8-distutils python3.8-venv pip -y

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN python3 setup.py install



EXPOSE 5000
WORKDIR /app/src/run
ENV FLASK_APP=app.py


#ENTRYPOINT ["python3"]
#CMD [ "src/run/application.py" ]
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]