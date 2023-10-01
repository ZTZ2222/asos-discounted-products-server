FROM python:3.10-slim
WORKDIR /project

# Set environment variables for Python and unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat-traditional instead of netcat
RUN apt-get update && apt-get install -y netcat-traditional

# Copy the rest of your application code into the container
COPY . .

# Entrypoint
ENTRYPOINT [ "sh", "entrypoint.sh" ]
