FROM ubuntu:18.04
# can you make it worse? :) 
RUN apt update && apt install -y python3 python3-pip locales && locale-gen en_US.UTF-8
ENV        LC_ALL=en_US.UTF-8
ENV        LANG=en_US.UTF-8
ENV        LANGUAGE=en_US.UTF-8
WORKDIR /opt/vulnapi
COPY . /opt/vulnapi
RUN pip3 install -r requirements.txt
ENTRYPOINT  ["./run.sh"]
