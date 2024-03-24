#!/bin/sh
podman  build \
--build-arg "host_uid=$(id -u)" \
--build-arg "host_gid=$(id -g)" \
--storage-driver=overlay \
--tag "mini:qemu" .

