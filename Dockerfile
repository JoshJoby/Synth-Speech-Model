# FROM rapidsai/rapidsai:23.06-cuda11.8-runtime-ubuntu22.04-py3.10
FROM python:3.10-slim
# Set the working directory
WORKDIR /app

# Install Azure CLI
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up environment variables for Azure Storage account
ENV AZ_STORAGE_ACCOUNT_NAME=synthspeechmodel
ENV AZ_STORAGE_ACCOUNT_KEY=2tYMclaD8PFFEckTUc5XVImKiECT454DaS7pqqHmj9eTU0vIOxuuXsBSy5Y0jnIB4F5t2/eW+WP++AStJM5/Dw==
ENV AZ_STORAGE_CONTAINER_NAME=synthspeechmodel
ENV AZ_STORAGE_BLOB_NAME=trained_random_forest_model_1000.pkl
ENV AZ_STORAGE_FILE_PATH=/app/trained_random_forest_model_1000.pkl
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV CUDA_PATH=/usr/local/cuda


# Modify CMD to check if the file exists, if not, download it
CMD [ "sh", "-c", "if [ ! -f $AZ_STORAGE_FILE_PATH ]; then az storage blob download --account-name $AZ_STORAGE_ACCOUNT_NAME --account-key $AZ_STORAGE_ACCOUNT_KEY --container-name $AZ_STORAGE_CONTAINER_NAME --name $AZ_STORAGE_BLOB_NAME --file $AZ_STORAGE_FILE_PATH; fi; python app.py" ]
