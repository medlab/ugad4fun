#!/bin/bash
sudo docker run \
--name=gt1 \
--publish=9002:9002 \
--publish=9080:9080 \
--publish=8002:8002  \
--publish=9001:9001 \
--volume=$(pwd)/../ugad4fun/recon_config:/usr/local/lib/python3.8/dist-packages/ugad4fun/recon_config \
--volume=$(pwd)/../ugad4fun/recon:/usr/local/lib/python3.8/dist-packages/ugad4fun/recon \
--rm -it gadgetron_uih:v1 /usr/local/bin/gadgetron
