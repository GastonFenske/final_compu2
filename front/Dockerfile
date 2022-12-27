# FROM node:16-alpine3.11
FROM node:alpine

WORKDIR /app

# COPY package.json .
# COPY yarn.lock .

# RUN apk add python3

RUN apk add --update python3 make g++\
   && rm -rf /var/cache/apk/*

# RUN yarn install --production

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build 

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]

# RUN yarn build

# RUN npm run build 

# EXPOSE 5173

# CMD ["yarn", "dev"]

# RUN apt-get update || : && apt-get install python -y

# RUN apk add python3

# RUN npm install -g yarn

# RUN yarn install
# RUN npm install -g npm@9.2.0
# RUN npm install

# CMD ["npm", "run", "dev"]