#!/bin/bash
wget https://buildroot.org/downloads/buildroot-2024.02.tar.xz
tar -xJf buildroot-2024.02.tar.xz
cd buildroot-2024.02
cp ../br_config ./.config
make

