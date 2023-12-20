FROM python:3.10-alpine

ENV PYTHONNUMBUFFERED 1
RUN pip install --upgrade pip

RUN mkdir /code
WORKDIR /code
# RUN pip install --no-cache-dir --upgrade pip && \
    # pip install --no-cache-dir -r requirements.txt

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code 

# RUN python manage.py makemigrations && manage.py migrate 
# ENTRYPOINT [ "sh", "entrypoint.sh" ]
# RUN chmod +x entrypoint.sh

# EXPOSE 8000

# CMD ["gunicorn","credit_approval_system.wsgi:application","--bind","0.0.0.0:8000"]


