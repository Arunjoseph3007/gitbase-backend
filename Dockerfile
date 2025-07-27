FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
EXPOSE 8080

# Install deps and get code
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
COPY . .
COPY scripts/ /usr/local/bin/

RUN python manage.py makemigrations
RUN python manage.py migrate

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]