# Use standard python image that implicitly contains build-essential tools instead of installing them via broken slim apt-cache
FROM python:3.11-bullseye

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .



# Run the Streamlit dashboard
ENTRYPOINT ["sh", "-c", "streamlit run dashboard.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
