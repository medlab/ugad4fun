#!/bin/bash
sudo docker run \
--name=gt1 \
--publish=9002:9002 \
--publish=9080:9080 \
--publish=8002:8002  \
--publish=9001:9001 \
--volume=$(pwd)/gadgetron/config:/usr/local/share/gadgetron/config \
--volume=$(pwd)/gadgetron/python:/usr/local/share/gadgetron/python \
--rm -it gadgetron_new:v1 /usr/local/bin/gadgetron