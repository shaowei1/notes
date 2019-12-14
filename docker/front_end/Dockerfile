FROM node:8.10.0 AS builder

COPY . /app
WORKDIR /app

RUN npm config set registry "https://registry.npm.taobao.org/" \
    && npm config set sass_binary_site=https://npm.taobao.org/mirrors/node-sass/ \
    && npm install \
    && npm run build:dev


FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
