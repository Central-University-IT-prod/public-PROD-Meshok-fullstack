FROM node:20-slim

WORKDIR /usr/src/nuxt_server/

COPY package*.json ./

RUN npm ci

RUN npm install typescript -g
RUN npm install nuxi -g

COPY . .

EXPOSE 3000 3000

RUN nuxt build

FROM node:20-alpine

COPY --from=0 /usr/src/nuxt_server/.output /usr/src/nuxt_server/.output

WORKDIR /usr/src/nuxt_server

# Host app
CMD [ "node", ".output/server/index.mjs" ]