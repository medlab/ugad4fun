FROM gadgetron/ubuntu_2004 AS gadgetron_image
LABEL org.opencontainers.image.authors="Xiannan.Cao"

EXPOSE 8002
EXPOSE 9001
EXPOSE 9002
EXPOSE 9080

COPY ./gadgetron_data/config/*.xml /usr/local/share/gadgetron/config/
COPY ./gadgetron_data/python/*.py /usr/local/share/gadgetron/python/
COPY ./gadgetron_data/pynufft-2022.2.3-py3-none-any.whl /tmp/gadgetron_data/

RUN cd /tmp/gadgetron_data &&\
 pip install pynufft-2022.2.3-py3-none-any.whl