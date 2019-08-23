FROM python:3.7.3
ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r packages.pip
CMD ["python", "app/app.py"]