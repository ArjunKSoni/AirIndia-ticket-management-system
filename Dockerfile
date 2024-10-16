FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "airindia.wsgi:application"]