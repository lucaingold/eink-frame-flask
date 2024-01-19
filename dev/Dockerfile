## Use the official Python image as the base image
#FROM python:latest
#
## Expose any necessary ports (if applicable)
#EXPOSE 8080
#
# # Set the working directory
#RUN mkdir /app
#WORKDIR /app
#
## Install git and additional packages
#RUN apt-get update && \
#    apt-get install -y git python3-venv && \
#    apt-get install -y libpq-dev && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
## Set up a virtual environment
#RUN python3 -m venv --system-site-packages .venv
#
## Activate the virtual environment
#SHELL ["/bin/bash", "-c"]
#RUN source .venv/bin/activate
#
## Install the specified Python packages
#RUN pip3 install \
#    git+https://github.com/robweber/omni-epd.git#egg=omni-epd
#COPY ../requirements.txt /app/requirements.txt
#RUN pip3 install -r requirements.txt
#
#
#
#
## Set the entry point, for example, to run a Flask app
## ENTRYPOINT ["python", "your_flask_app.py"]
#
#COPY .. /app
#
## Command to run when the container starts
##CMD ["bash"]
#CMD python3 app.py