FROM python:3.12-slim

WORKDIR /opt/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . /opt/app

# Copy the entrypoint script
COPY entrypoint.sh /opt/app/entrypoint.sh

# Make the entrypoint executable
RUN chmod +x /opt/app/entrypoint.sh

# Use the entrypoint script as the container CMD
CMD ["/opt/app/entrypoint.sh"]
