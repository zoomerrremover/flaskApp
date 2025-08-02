FROM python:3.10.18-alpine3.21

RUN apk add curl

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ src/

ENV PYTHONPATH="/app:$PYTHONPATH"

COPY run.py .
CMD ["flask", "--app=run", "run", "--host=0.0.0.0", "--port=8080"] 
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:run"]
