# pull official base image
FROM python:3.9.7

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# copy project
COPY . .

CMD ["sh", "-c", "flask db upgrade ; python3 pywsgi.py"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# CMD gunicorn --worker-class gevent \
#   --workers 1 \
#   --bind 0.0.0.0:5000 \
#   main:app