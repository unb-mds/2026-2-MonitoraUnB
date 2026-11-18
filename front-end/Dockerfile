# Etapa 1: Compilação do TypeScript
FROM node:22-alpine AS build

WORKDIR /app

COPY front-end/package.json front-end/package-lock.json ./

RUN npm ci

COPY front-end/ ./

RUN npx tsc


# Etapa 2: Servidor web
FROM nginx:alpine

RUN rm -f /usr/share/nginx/html/index.html

COPY --from=build /app/pages /usr/share/nginx/html/pages

COPY --from=build /app/styles /usr/share/nginx/html/styles

COPY --from=build /app/dist /usr/share/nginx/html/dist

# Não copiar inicio.html para a raiz: os hrefs relativos (inscricao.html etc.)
# e os ../styles|../dist só funcionam sob /pages/.
COPY front-end/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
