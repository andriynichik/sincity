FROM python:3.6.1

RUN apt-get update -y

RUN python -m pip install pymongo==3.4.0

RUN python -m pip install geopy==1.11.0

RUN pip3 install beautifulsoup4

RUN python -m pip install pyyaml==3.12

RUN python -m pip install matplotlib==2.0.1

RUN python -m pip install pandas==0.20.3

RUN pip install -U googlemaps==2.5.1

RUN pip install Flask==0.12.2

ENV PYTHONPATH "$PYTHONPATH:/app/"
ENV PYTHONIOENCODING "utf-8"
ENV FLASK_APP "/app/client/index.py"
ENV FLASK_DEBUG 1

WORKDIR /app

RUN git clone https://github.com/bpteam/WebCrawler_FR.git .

CMD ["flask", "run", "--host=0.0.0.0"]