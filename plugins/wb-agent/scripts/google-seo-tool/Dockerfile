FROM node:20-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install dependencies using npm ci
RUN npm ci

# Copy codebase
COPY . .

# Set correct ownership
RUN chown -R node:node /usr/src/app

# Run as non-root user
USER node

# Default entrypoint/command
CMD ["node", "index.js"]
