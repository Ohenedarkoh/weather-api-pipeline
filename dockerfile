FROM apache/airflow:3.3.2

COPY requirements.txt /requirements.txt
#copies the dependency list into the image

RUN pip install --no-cache-dir -r /requirements.txt
#installs the required python packages
