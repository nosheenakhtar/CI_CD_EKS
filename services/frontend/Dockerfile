# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --production || npm install --production
COPY . .
ENV PORT=3000 BACKEND_URL=http://backend:5000
EXPOSE 3000
CMD ["npm", "start"]
