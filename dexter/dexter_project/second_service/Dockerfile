FROM python3.8:latest


# Set environment  variables
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

# Upgrade pip
RUN pip install pip==23.1.2

RUN apt-get update

# Required for pyaudio
RUN apt-get install portaudio19-dev python-all-dev -y 

# Install requirements.
RUN pip install --no-cache-dir -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code
# RUN cd ..
# RUN ls
# RUN python3 manage.py runserver    
