#!/bin/bash
docker run \
--name=gt1 \
--publish=9002:9002 \
--publish=9080:9080 \
--publish=8002:8002 \
--publish=9001:9001 \
--volume=/gadgetron_data:/tmp/gadgetron_data \
--volume=/gadgetron/config:/usr/local/share/gadgetron/config \
--volume=/gadgetron/python:/usr/local/share/gadgetron/python \
--rm -it gadgetron/ubuntu_2004 /usr/local/bin/gadgetron