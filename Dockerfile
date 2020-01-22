FROM python:3.7
# can you make it worse? :) 
WORKDIR /opt/vulnapi
COPY . /opt/vulnapi
RUN pip install -r requirements.txt
ENTRYPOINT  ["./run.sh"]
