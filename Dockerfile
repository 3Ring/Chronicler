# FROM python:3.7.11-slim-buster

# # WORKDIR /chronicler
# COPY setup.py .
# RUN pip install -e .
# COPY requirements.txt .
# RUN python -m pip install --upgrade pip
# RUN pip3 install -r requirements.txt && \
#     pip install psycopg2-binary 
# COPY . .
# CMD [ "gunicorn", "--reload", "-b", "0.0.0.0:5000", "--chdir", "/project", "--worker-class", "eventlet", "-w", "1", "app:app" ]

# FROM python:3.7.11-slim-buster

# WORKDIR /app
# COPY requirements.txt .
# RUN python -m pip install --upgrade pip
# RUN pip3 install -r requirements.txt && \
#     pip install psycopg2-binary
# COPY . .
# CMD [ "gunicorn", "--reload", "-b", "0.0.0.0:5000", "--worker-class", "eventlet", "-w", "1", "app:app" ]

FROM python:3.7.11-slim-buster


WORKDIR /app
COPY setup.py .
RUN pip install -e .
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt && \
    pip install psycopg2-binary && \
    python -m pip install requests
COPY . .
CMD [ "gunicorn", "--reload", "-b", "0.0.0.0:5000", "--worker-class", "eventlet", "-w", "1", "app:app()" ]