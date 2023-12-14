FROM python:3.8-alpine
ENV PYTHONNUNBUFFERED 1

WORKDIR /worker

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python", "worker.py"]