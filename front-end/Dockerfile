# Etapa 1: Compilação do TypeScript
FROM node:22-alpine AS build

WORKDIR /app

COPY front-end/package.json front-end/package-lock.json ./

RUN npm ci

COPY front-end/ ./

# Compila o TypeScript
RUN npx tsc


# Etapa 2: Servidor Nginx
FROM nginx:alpine

RUN rm -f /usr/share/nginx/html/index.html

COPY front-end/nginx/default.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/pages /usr/share/nginx/html/pages

COPY --from=build /app/styles /usr/share/nginx/html/styles

COPY --from=build /app/dist /usr/share/nginx/html/dist

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
