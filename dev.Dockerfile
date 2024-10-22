# Use an official Python runtime as a parent image
FROM python:3.8-buster

# Set the working directory to /pulsepoint
WORKDIR /pulsepoint

# Copy the requirements file into the container at /pulsepoint
COPY requirements.txt /pulsepoint/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Copy the rest of the application code into the container at /pulsepoint
COPY . /pulsepoint/

# Set environment variables (adjust as needed)
ENV DJANGO_SETTINGS_MODULE=pulsepoint.settings
ENV DEBUG=False

# Expose port 8000 for the Django app
EXPOSE 8000

# Copy the entrypoint script into the container at /pulsepoint
COPY entrypoint.sh /pulsepoint/entrypoint.sh
RUN chmod +x /pulsepoint/entrypoint.sh

# Start the Django development server using the entrypoint script
CMD ["/pulsepoint/entrypoint.sh"]