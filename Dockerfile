# base image
FROM python:3.10.9

# workdir
WORKDIR /app

# copy
COPY . /app

# run
RUN pip install -r requirements.txt

# port
EXPOSE 8000

# command

CMD ["python", "./app_interface.py"]


