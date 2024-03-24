#!/bin/bash
( 
  export PATH_TO_LIBGPIOD=/home/dev/libgpiod-2.1
  cd ~/demo
  xfce4-terminal -H -x ./rungui &
  # Wait some time so that GUI starts.
  sleep 3
  cd vhost-device/target/debug
  LD_LIBRARY_PATH=${PATH_TO_LIBGPIOD}/lib/.libs ./vhost-device-gpio -l s1 -s /tmp/gpio.sock
)
