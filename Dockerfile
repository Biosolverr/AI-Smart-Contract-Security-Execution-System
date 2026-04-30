# Multi-stage build for GenRoute AI

FROM python:3.10-slim as backend

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

EXPOSE 8000
CMD ["python", "main.py"]

# --- Frontend Stage ---
FROM node:18-alpine as frontend

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
