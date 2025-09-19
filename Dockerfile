# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
# This will copy the healthcare-patient folder and static
COPY . .

# Set environment variable for port
ENV PORT 8501

# Run the Streamlit app
CMD exec streamlit run app.py --server.port=$PORT --server.address=0.0.0.0