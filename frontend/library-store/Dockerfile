# Use an official Node runtime as the base image
FROM node:18 AS build_stage
# Set the working directory in the container
WORKDIR /app
# Copy package.json and package-lock.json
COPY package*.json ./
# Install dependencies
RUN npm install
# Copy the rest of the application code
COPY . .
# Build the app
RUN npm run build
# Install a simple http server for serving static content
RUN npm install -g serve


# Using alpine image of node
FROM node:18.20.4-alpine3.20
# Adding Labels
LABEL image="frontend"
# Adding argument statements for user and homedirectory
ARG USERNAME='library'
ARG HOMEDIR='/library'
# Creating user and homedirectory
RUN adduser -h ${HOMEDIR} -s /bin/sh -D ${USERNAME}
# Adding user and assigning new working directory
USER ${USERNAME}
WORKDIR ${HOMEDIR}
# Copying the frontend files from building_stage
COPY --from=build_stage --chown=${USERNAME}:${USERNAME} /app/public "${HOMEDIR}/public"
# Make port 3000 available to the world outside this container
EXPOSE 3000
# Run the app when the container launches
CMD ["serve", "-s", "build", "-l", "3000"]
