# gpio-qemu-demo
This repository contains the files used to demonstrate the emulation of GPIO in QEMU based
on the [vhost-device](https://github.com/rust-vmm/vhost-device). 
I have slightly modified the original implementation and published it in [my fork, branch gpio-python](https://github.com/wzab/vhost-device/tree/gpio-python).

## How to prepare the demo on Linux
* Check out the repository. Go to the `gpio-qemu-demu/podman` subdirectory.
* Run the script `build.sh` there. Building the image may be quite long, as it includes also compilation of the Buildroot Linux image.
## How to run the demo on Linux
* Run the scipt `runme.sh` in directory `gpio-qemu-demu/podman`
* You should get the text console of the running container with the prompt like: ``
* Run `. runvnc` or `source runvnc`. After that you'll be able to connect via VNC to the GUI of the container.
* *On your workstation* run `vncviewer :7` or similar comman allowing you to connect to the container via VNC.

