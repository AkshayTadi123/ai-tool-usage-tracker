# Stage 1: build the static bundle with Node.
FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

COPY . .
RUN npx ng build

# Stage 2: serve it with nginx. Node is not in the final image, so the
# published image is a few MB of static files instead of a toolchain.
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
