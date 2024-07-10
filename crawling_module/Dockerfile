FROM python:3.12-slim as base

# Set the working directory
WORKDIR /app

# Copy the requirements file

COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY /crawling_movies .


ENTRYPOINT [ "python", "crawling_movies/run_spiders.py"]

