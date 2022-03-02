FROM python:latest
COPY . /usr/app/MNIST
WORKDIR /usr/app/MNIST
ADD mnistApp.py .
RUN pip install --upgrade pip
RUN pip install -r requirementsFinal.txt
EXPOSE 8000
ENV FLASK_APP=mnistApp:app
CMD ["flask", "run", "--host", "0.0.0.0"]
