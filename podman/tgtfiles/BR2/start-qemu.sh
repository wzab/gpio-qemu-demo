#!/bin/sh

BINARIES_DIR="${0%/*}/"
# shellcheck disable=SC2164
cd "${BINARIES_DIR}"

mode_serial=false
mode_sys_qemu=false
while [ "$1" ]; do
    case "$1" in
    --serial-only|serial-only) mode_serial=true; shift;;
    --use-system-qemu) mode_sys_qemu=true; shift;;
    --) shift; break;;
    *) echo "unknown option: $1" >&2; exit 1;;
    esac
done

if ${mode_serial}; then
    EXTRA_ARGS='-nographic'
else
    EXTRA_ARGS=''
fi

if ! ${mode_sys_qemu}; then
    export PATH="/home/dev/demo/BR2/buildroot-2024.02/output/host/bin:${PATH}"
fi

cd /home/dev/demo/BR2/buildroot-2024.02/output/images
exec qemu-system-aarch64 -M virt -m 1G -cpu cortex-a53 -nographic \
-chardev socket,path=/tmp/gpio.sock0,id=vgpio \
-device vhost-user-gpio-pci,chardev=vgpio,id=gpio \
-object memory-backend-file,id=mem,size=1G,mem-path=/tmp,share=on \
-numa node,memdev=mem  \
-smp 1 -kernel Image -append "rootwait root=/dev/vda console=ttyAMA0" \
-netdev user,hostfwd=tcp::8888-:8888,id=eth0 -device virtio-net-device,netdev=eth0 \
-drive file=rootfs.ext4,if=none,format=raw,id=hd0 \
-device virtio-blk-device,drive=hd0  ${EXTRA_ARGS} "$@"

