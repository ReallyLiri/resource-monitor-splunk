FROM python:3.6

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY monitor_worker.py /monitor_worker.py
COPY monitor.sh /monitor.sh
COPY config.json /config.json

RUN chmod +x /monitor.sh
RUN chmod +x /monitor_worker.py

CMD ["/monitor.sh"]
