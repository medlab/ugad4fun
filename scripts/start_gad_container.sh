#!/bin/bash
sudo docker run \
--name=gt1 \
--publish=9002:9002 \
--publish=9080:9080 \
--publish=8002:8002  \
--publish=9001:9001 \
--rm -it gadgetron_uih:v1 /usr/local/bin/gadgetron