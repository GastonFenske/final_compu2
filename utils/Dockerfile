FROM node:alpine

WORKDIR /app

RUN apk add --update python3 make g++\
   && rm -rf /var/cache/apk/*

COPY package*.json .

RUN npm install

COPY . .


EXPOSE 8000

CMD ["node", "adapter2.js"]