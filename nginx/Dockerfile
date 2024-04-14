FROM nginx:1.25.3

RUN apt install curl

EXPOSE 80

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
