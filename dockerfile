FROM ubuntu:22.04

# Set the working directory in the container
WORKDIR /app

# Update the package manager and install necessary packages
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-dev build-essential libpq-dev vim unzip

# Install additional system packages if needed
# For example, if you need to use PostgreSQL as your database, you can add the following line:
# RUN apt-get install -y postgresql

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install pyOpenSSL
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt install openssl
RUN pip3 install --upgrade pyOpenSSL


# Copy your Django project files into the container
COPY . .

# Expose the port that Django runs on (optional, if you are running the container as a web server)
EXPOSE 8000

# Define the command to run your Django application using the development server (replace "myproject" with your Django project name)
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
RUN chmod +x start.sh
ENTRYPOINT ["/app/start.sh"]