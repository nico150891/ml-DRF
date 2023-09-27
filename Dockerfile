# Base image  
FROM python:3.10.12

# Setup environment variable  
ENV DockerHOME=/home/app

# Set work directory  
RUN mkdir -p $DockerHOME

# Switch cursor to work directory  
WORKDIR $DockerHOME

# Set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt requirements.txt 
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    ffmpeg \
    libsm6  \
    libxext6 " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false "build-essential" \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the project
COPY . .

# Expose the application server's port  
EXPOSE 8000

# Run the entrypoint file
ENTRYPOINT ["./django.sh"]