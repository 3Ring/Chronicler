FROM python:3.7.11-slim-buster

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .

# local gunicorn
CMD [ "gunicorn", "--reload", "-b", "0.0.0.0:5000", "--worker-class", "eventlet", "-w", "1", "app:app"]

# local flask
# CMD [ "python3", "-m" , "flask", "run", "--host", "0.0.0.0"]