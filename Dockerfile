FROM python:3.9-slim

# Install dependencies for Chromium and Playwright
RUN apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libasound2 libpangocairo-1.0-0 libgbm1 libatk1.0-0 libcups2 libdrm2 libxshmfence1 libxss1 fonts-liberation wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium

# Copy app code
COPY . .

# Expose port (default Flask port)
EXPOSE 8000

# Run Flask app
CMD ["python", "app.py"]
