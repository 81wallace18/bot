# Use an official Node.js runtime as a parent image
FROM node:18-slim

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
CMD ["node", "index.js"]z