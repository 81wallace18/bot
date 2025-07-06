# Use an official Node.js runtime with Chrome
FROM node:18-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-liberation \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for Puppeteer to use installed Chrome
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if any) to the working directory
COPY package.json ./

# Install any needed packages
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Make port 3000 available to the world outside this container (adjust if your Node.js app uses a different port)
EXPOSE 3000

# Run the index.js file when the container launches
CMD ["node", "index.js"]