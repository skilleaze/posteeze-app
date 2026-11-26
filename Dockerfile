# Posteeze: built from this repo's source (rebranded Postiz v2.26.0).
# nginx :5000 fronts the frontend :4200, backend :3000 and the Temporal worker.
FROM node:22.23.4-bookworm-slim
ARG NEXT_PUBLIC_VERSION=posteeze-2.26.0
ENV NEXT_PUBLIC_VERSION=$NEXT_PUBLIC_VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ make python3-pip bash nginx ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN addgroup --system www \
 && adduser --system --ingroup www --home /www --shell /usr/sbin/nologin www \
 && mkdir -p /www /uploads \
 && chown -R www:www /www /var/lib/nginx
RUN npm --no-update-notifier --no-fund --global install pnpm@10.6.1 pm2
WORKDIR /app
COPY . /app
COPY var/docker/nginx.conf /etc/nginx/nginx.conf

# Session cookie on the exact host (not the parent domain).
RUN sed -i 's|^\(\s*\)server_name _;|&\n\1proxy_cookie_domain ~. $host;|' /etc/nginx/nginx.conf \
 && grep -q proxy_cookie_domain /etc/nginx/nginx.conf && nginx -t

RUN pnpm install --frozen-lockfile
RUN NODE_OPTIONS="--max-old-space-size=6144" pnpm run build

ENV IS_GENERAL=true \
    BACKEND_INTERNAL_URL=http://localhost:3000 \
    STORAGE_PROVIDER=local \
    UPLOAD_DIRECTORY=/uploads \
    NEXT_PUBLIC_UPLOAD_DIRECTORY=/uploads
EXPOSE 5000
# Railway's PORT (5000) belongs to nginx; the backend gets 3000.
CMD ["sh", "-c", "nginx && PORT=3000 exec pnpm run pm2"]
