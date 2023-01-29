# Dockerfile
FROM python:3.8-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /food-suggestion-app-backend
WORKDIR /food-suggestion-app-backend
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]