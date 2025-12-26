code.language: docker
-
tag(): user.code_comment_line

# Docker instruction commands
state from: "FROM "
state run: "RUN "
state copy: "COPY "
state add: "ADD "
state work dir: "WORKDIR "
state expose: "EXPOSE "
state command: "CMD "
state entry point: "ENTRYPOINT "
state env: "ENV "
state arg: "ARG "
state label: "LABEL "
state volume: "VOLUME "
state user: "USER "
state health check: "HEALTHCHECK "
state shell: "SHELL "
state on build: "ONBUILD "
state stop signal: "STOPSIGNAL "
state maintainer: "MAINTAINER "

# Common patterns
state from ubuntu: "FROM ubuntu:"
state from alpine: "FROM alpine:"
state from debian: "FROM debian:"
state from node: "FROM node:"
state from python: "FROM python:"
state from nginx: "FROM nginx:"
state copy from: "COPY --from="
state run apt update: "RUN apt-get update && apt-get install -y "
state run apk add: "RUN apk add --no-cache "
state run pip install: "RUN pip install "
state run npm install: "RUN npm install "
state cmd exec: "CMD ["
state entrypoint exec: "ENTRYPOINT ["
