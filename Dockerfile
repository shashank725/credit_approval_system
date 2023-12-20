FROM python:3.10

ENV PYTHONNUMBUFFERED 1
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /code
# RUN pip install --no-cache-dir --upgrade pip && \
    # pip install --no-cache-dir -r requirements.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python manage.py makemigrations && manage.py migrate 
# ENTRYPOINT [ "sh", "entrypoint.sh" ]
# RUN chmod +x entrypoint.sh

# EXPOSE 8000

# CMD ["gunicorn","credit_approval_system.wsgi:application","--bind","0.0.0.0:8000"]


