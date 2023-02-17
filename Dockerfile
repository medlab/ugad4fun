FROM gadgetron/ubuntu_2004 AS gadgetron_image

# expose ports
EXPOSE 8002
EXPOSE 9001
EXPOSE 9002
EXPOSE 9080

# copy dir and fils to docker image
COPY ./ /tmp/ugad4fun/

# install pynufft
RUN cd /tmp/ugad4fun &&\
 pip install . &&\
 ln -s /usr/local/lib/python3.8/dist-packages/ugad4fun/recon_config /usr/local/share/gadgetron/config/recon_config