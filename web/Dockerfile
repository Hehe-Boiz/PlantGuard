FROM node:22.16.0

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

RUN chmod +x /app/node_modules/.bin/*

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]