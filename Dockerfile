FROM python:alpine3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
EXPOSE 5107
CMD ["python","main.py"]