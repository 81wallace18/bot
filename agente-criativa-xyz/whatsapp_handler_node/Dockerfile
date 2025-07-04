# Use an official Node.js runtime as a parent image
FROM node:18-slim

# Install required libraries for Puppeteer
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if any) to the working directory
COPY package*.json ./

# Install any needed packages
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Make port 3000 available to the world outside this container (adjust if your Node.js app uses a different port)
EXPOSE 3000

# Run the index.js file when the container launches
CMD ["node", "index.js"]

