FROM python:latest
RUN pip3 install bottle
RUN pip3 install sqlite3
COPY TryToBottle.py.py /home/TryToBottle.py
COPY DataBaseForRestGuy.py /home/DataBaseForRestGuy.py
COPY Base.db /home/Base.db
WORKDIR /home

EXPOSE 8080

CMD [ "python3", "./TryToBottle.py" ]