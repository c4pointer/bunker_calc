FROM python:3.9
LABEL authors="oleg"

WORKDIR /app
ADD main.py create_vessel.py db_editing.py db_reading.py vol_coorection.py requirements.txt ./
ADD viking_ocean.db viking_sea.db bunkercalc.kv ./

RUN  pip install -r requirements.txt

CMD ["python", "./main.py"]
