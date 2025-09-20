tag: terminal
and tag: user.docker
-
docker {user.docker_command} [<user.docker_arguments>]:
    args = docker_arguments or ""
    "docker {docker_command}{args} "
docker run [<user.docker_arguments>] [<user.text>]:
    args = docker_arguments or ""
    image = text or ""
    user.insert_between('docker run{args} {image}', '')
docker exec [<user.docker_arguments>] [<user.text>]:
    args = docker_arguments or ""
    container = text or ""
    user.insert_between('docker exec{args} {container}', '')
docker build [<user.docker_arguments>] tag [<user.text>]:
    args = docker_arguments or ""
    tag = text or ""
    user.insert_between('docker build{args} --tag {tag}', '')

# Optimistic execution for frequently used commands that are harmless (don't
# change container or image state).
docker ps$: "docker ps\n"
docker ps all$: "docker ps -a\n"
docker images$: "docker images\n"
docker version$: "docker version\n"
docker info$: "docker info\n"
docker system df$: "docker system df\n"
docker system prune dry run$: "docker system prune --dry-run\n"

# Docker Compose
docker compose up$: "docker compose up\n"
docker compose down$: "docker compose down\n"
docker compose down then up$: "docker compose down && docker compose up\n"

# Convenience
docker run clipboard:
    insert("docker run ")
    edit.paste()
docker pull clipboard:
    insert("docker pull ")
    edit.paste()
    key(enter)
docker push clipboard:
    insert("docker push ")
    edit.paste()
    key(enter)
docker exec clipboard:
    insert("docker exec -it ")
    edit.paste()
    insert(" /bin/bash")
docker logs clipboard:
    insert("docker logs ")
    edit.paste()
    key(enter)
docker stop clipboard:
    insert("docker stop ")
    edit.paste()
    key(enter)
docker rm clipboard:
    insert("docker rm ")
    edit.paste()
    key(enter)
docker rmi clipboard:
    insert("docker rmi ")
    edit.paste()
    key(enter)
docker build clipboard:
    insert("docker build -t ")
    edit.paste()
    insert(" .")
docker run highlighted:
    edit.copy()
    insert("docker run ")
    edit.paste()
docker exec highlighted:
    edit.copy()
    insert("docker exec -it ")
    edit.paste()
    insert(" /bin/bash")
docker logs highlighted:
    edit.copy()
    insert("docker logs ")
    edit.paste()
    key(enter)
docker stop highlighted:
    edit.copy()
    insert("docker stop ")
    edit.paste()
    key(enter)
docker rm highlighted:
    edit.copy()
    insert("docker rm ")
    edit.paste()
    key(enter)
docker rmi highlighted:
    edit.copy()
    insert("docker rmi ")
    edit.paste()
    key(enter)
