FROM debian:10
RUN apt-get update
RUN apt-get install -y git sqlite3 python3 python3-pip procps
RUN python3 -m pip install jupyter pandas sqlalchemy
RUN python3 -m pip install logica

COPY python python
COPY db db

ENV PYTHONPATH /python
CMD ["/usr/local/bin/jupyter", "notebook", "--notebook-dir=/notebook", "--port=8888", "--no-browser", "--ip=*", "--allow-root"]
