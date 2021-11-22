FROM nginx:1.21.4

RUN  rm -rf /etc/nginx/conf.d/default.conf

COPY conf.d/proxy.conf /etc/nginx/conf.d/proxy.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]