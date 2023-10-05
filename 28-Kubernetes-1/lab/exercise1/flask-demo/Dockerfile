FROM python:3.7-alpine

RUN mkdir /app

WORKDIR /app 

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app.py ./
RUN chmod 644 app.py

EXPOSE 5000

LABEL maintainer = "Jevon van Dijk"
LABEL version = "k8s"

ENTRYPOINT ["python"]
CMD ["app.py"]
