FROM rapidsai/rapidsai:23.06-cuda11.8-runtime-ubuntu22.04-py3.10

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app



# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Modify CMD to directly activate the Conda environment and run your application
CMD [ "python", "app.py"]
