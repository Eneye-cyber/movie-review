FROM node:20

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the code
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
