FROM python:3.10-alpine

WORKDIR /bot

COPY requirements.txt .
RUN pip install -r requirements.txt 

CMD ["python", "main.py"]