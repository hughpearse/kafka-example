FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
RUN pip3 install -r requirements.txt
CMD ["python3", "/app/app.py"]
