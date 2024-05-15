# # Base image with Python and dependencies
# FROM python:3.8-slim

# # Install TorchServe dependencies
# RUN pip install torchserve

# # Set working directory
# WORKDIR /app

# # Copy Mistral model and configuration (replace with your paths)
# COPY model.bin model.config /app/model

# # Expose port for TorchServe (default 8080)
# EXPOSE 8080

# # Start TorchServe with the Mistral model
# CMD ["torchserve", "--start", "--model-name", "mistral", "--model-store", "/app/model"]