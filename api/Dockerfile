FROM ubi9/python-39

WORKDIR /usr/src/app

COPY server.py .
COPY requirements.txt .

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["server.py"]


