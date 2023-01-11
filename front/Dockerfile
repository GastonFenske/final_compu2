FROM node:alpine

WORKDIR /app


RUN apk add --update python3 make g++\
   && rm -rf /var/cache/apk/*

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build 

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]