# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install dependencies
RUN pip install --no-cache-dir flask yfinance pymongo apscheduler bson

# Step 5: Expose port 5000 for the Flask app
EXPOSE 5000

# Step 6: Run the application
CMD ["python", "app.py"]
