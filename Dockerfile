FROM python:3.14-slim

RUN apt-get update
RUN pip install --upgrade pip
COPY requirements.txt dev-requirements.txt ./
RUN pip install -r requirements.txt && pip install -r dev-requirements.txt
COPY ./ ./

CMD ["python", "main.py"]
