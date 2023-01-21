FROM python:3.10.5-bullseye

WORKDIR /challenge-stori

COPY ./requirements.txt /Reto_Cidenet/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /Reto_Cidenet/app
 
COPY .env /Reto_Cidenet/.env

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/Reto_Cidenet/app"

CMD ["uvicorn", "-b", "0.0.0.0:8000", "app.main:app"]