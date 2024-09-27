# Stage 1: Build Stage
FROM python:3.11-alpine AS builder
# Set environment variables to avoid Python writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install necessary build dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev postgresql-dev
# Create a directory for the application
WORKDIR /users
# Copy the requirements file to install dependencies
COPY requirements.txt .
# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install setuptools==70.0.0


# Stage 2: Runtime Stage
FROM python:3.11-alpine
# Set environment variables to avoid Python writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install runtime dependencies, including PostgreSQL client libraries
RUN apk add --no-cache libpq
# Passing environmental variables to parameterize the application USERNAME AND WORKING DIRECTORY
ARG HOMEDIR='/users'
ARG USERNAME='users'
# Creating the user and assigning working directory to user
RUN adduser -h ${HOMEDIR} -s /bin/sh -D {USERNAME}
# Create a directory for the application
WORKDIR ${HOMEDIR}
USER ${USERNAME}
# Copy installed dependencies from the builder stage
COPY --from=builder --chown=${USERNAME}:${USERNAME} /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder --chown=${USERNAME}:${USERNAME} /usr/local/bin /usr/local/bin
# Copy the application source code to the working directory
COPY . .
# Ensure uvicorn is installed in case it wasn't properly copied or was missed
RUN pip install --no-cache-dir uvicorn
# Expose the port the app runs on
EXPOSE 8000
# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]