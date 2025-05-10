FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY predict.py .

RUN pip install -r requirements.txt

EXPOSE 9696

CMD ["python", "predict.py"]