FROM gcr.io/google-appengine/python

RUN apt-get update

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
RUN virtualenv /env -p python3.6

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV APP_HOME /app
ENV WORK_ROOT /data
ENV PATH /env/bin:$PATH
ENV PATH /usr/include/gdal:$PATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

# dependencies into the virtualenv.
RUN pip install --upgrade pip
RUN apt-get update 

# Copy the application's requirements.txt and run pip to install all
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add the application source code.
ADD . /app
WORKDIR $APP_HOME
COPY . ./
EXPOSE $PORT

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD gunicorn --bind :$PORT --workers 1 --threads 4 app:app

CMD [ "python","app.py"]