FROM python:3.6.1

RUN apt-get update -y \
    && python -m pip install pymongo==3.4.0 \
    && python -m pip install geopy==1.11.0 \
    && pip3 install beautifulsoup4 \
    && python -m pip install pyyaml==3.12 \
    && python -m pip install matplotlib==2.0.1 \
    && python -m pip install pandas==0.20.3 \
    && pip install -U googlemaps==2.5.1 \
    && pip install Flask==0.12.2 \
    && pip install flask-login==0.4.0 \
    && pip install Flask-WTF==0.14.2

ENV PYTHONPATH "$PYTHONPATH:/app/"
ENV PYTHONIOENCODING "utf-8"
ENV FLASK_APP /app/client/application/__init__.py
ENV FLASK_DEBUG 1

WORKDIR /app

CMD bash -c "pip install -e /app/client && flask run --host=0.0.0.0"