FROM python:latest
RUN pip3 install bottle
COPY TryToBottle.py /home/TryToBottle.py
COPY DataBaseForRestGuy.py /home/DataBaseForRestGuy.py
COPY Base.db /home/Base.db
WORKDIR /home

CMD [ "python3", "./TryToBottle.py" ]