# gpio-qemu-demo
This repository contains the files used to demonstrate the emulation of GPIO in QEMU based
on the [vhost-device](https://github.com/rust-vmm/vhost-device). 
I have slightly modified the original implementation and published it in [my fork, branch gpio-python](https://github.com/wzab/vhost-device/tree/gpio-python).
Please note that I use `podman` in my demo. If you want, you may use `docker` instead.

## How to prepare the demo on Linux
* Check out the repository. Go to the `gpio-qemu-demu/podman` subdirectory.
* Run the script `build.sh` there. Building the image may be quite long, as it includes also compilation of the Buildroot Linux image.
## How to run the demo on Linux
* Run the scipt `runme.sh` in directory `gpio-qemu-demu/podman`
* You should get the text console of the running container with the prompt like: `dev@ae2a28f71528:~$`
* Run `. runvnc` or `source runvnc`. After that you'll be able to connect via VNC to the GUI of the container.
* *On your workstation* run `vncviewer :7` or similar comman allowing you to connect to the container via VNC (the password is `test12`).
![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/9e43374d-433e-4637-85d6-397597bf1522)

## How to prepare and run the demo on Windows
It is possible to run my demo in `docker` on Windows. The repository contains the `build.bat` file for building the image, and `runme.bat` for starting the container.
Unfortunately, building the image is much slower on Windows than on Linux. *On my machine with 12-core Xeon and 64 GB of RAM, creating the image took 7500 seconds. During that time, 4900 seconds was spent on building Buildroot*.

You also need a VNC client for wndows (I use [TigerVNC](https://tigervnc.org/)).

## Running demo in the container's GUI
* Start two terminals in GUI.
  ![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/278020b0-ab00-4a30-972e-bcf90de177a7)
  
* In the first terminal go to the `~/demo` directory and run `./startgpio.sh` in that directory.
* The additional terminal with the RPC server should appear and the virtual board with LEDs, switches and buttons should be displayed.
![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/7d009b0d-22ec-4f92-adde-2dfd415603f7)

* In the second terminal go to the `~/demo/BR2` directory and run `./start-qemu.sh`. You should get the Buildroot prompt.
![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/31c59102-6373-49d5-b99d-122db2094419)

* Log as `root` (without password).
* Load the driver for the virtual GPIO with `modprobe virtio-gpio`
![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/74b80098-8946-484c-af2f-9c1e0854e581)

* After that you should be able to use `gpio...` commands to check the available GPIOs (e.g. via `gpioinfo`) switch on/off LEDs:
![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/711bf5d3-e0a2-499b-878e-87bd400a1b3c)

* You may also monitor the buttons with `gpiomon`:
![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/4462dda2-bd5f-429a-b2a2-f7017d1d326f)

Please note that my servicing of interrupts in Python is not perfect. Therefore, if you stop `gpiomon` with `CTRL+C`, you must once again activate the button to complete handling of the interrupt.
I hope to fix this issue in the future.

* The emulated GPIOs are also fully accessible via the old and obsolete sysfs interface (please note, that the base address for virtual GPIO is 480):
![obraz](https://github.com/wzab/gpio-qemu-demo/assets/2532225/a1355fa2-153f-44ac-a0b4-9d2cbdc8e75c)




  
