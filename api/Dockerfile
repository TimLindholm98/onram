FROM registry.access.redhat.com/ubi9/python-39

WORKDIR /usr/src/app

#RUN dnf install -y gcc python3-devel

ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/include/mysql -lmysqlclient"

RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .


EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["server.py"]


