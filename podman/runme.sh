#!/bin/sh
podman run -it \
  -p 127.0.0.1:5907:5907/tcp \
  -v $PWD/host:/home/dev/host \
  --device /dev/snd \
  mini:qemu

