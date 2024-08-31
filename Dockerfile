FROM python:latest

WORKDIR .

COPY influxdb_api.py ./
COPY mistapi.py ./

#ENV PATH="./vir/bin:$PATH"
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir requests urllib3
RUN pip install influxdb influxdb-client
ENTRYPOINT ["python","./influxdb_api.py"]