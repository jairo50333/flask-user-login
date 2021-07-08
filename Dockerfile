FROM python:3.8.8

RUN useradd --create-home userapi
WORKDIR lesson2.1/

RUN pip install -U pipenv
RUN pip install -U  pyjwt
RUN pip install -U psycopg2
RUN pipenv install pyjwt
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
COPY ./ .
RUN chown -R userapi:userapi ./
USER userapi

EXPOSE 8000
#EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
#CMD ["gunicorn","-b0.0.0.0:8000","wsgi:app"]
#CMD ["python","./wsgi.py"]