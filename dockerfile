# Stage 1: Use an official Python runtime as a parent image
FROM continuumio/miniconda3:latest AS base

# Set the working directory in the container
WORKDIR /app

# Copy the conda environment file to the container at /app
COPY environment.yml /app/environment.yml

# Create the conda environment
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "synth-env", "/bin/bash", "-c"]

# Stage 2: Use the conda environment from Stage 1
FROM base AS final

# Copy the local code to the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 8080

# Define environment variable
ENV NAME World

# Command to run on container start
CMD ["conda", "run", "--no-capture-output", "-n", "synth-env", "python", "app.py"]
