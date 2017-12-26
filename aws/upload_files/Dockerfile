FROM ubuntu:latest
LABEL "maintainer"="ialmandos@conatel.com.uy"
RUN apt-get update && apt-get install -y python3 python3-pip
RUN echo "alias python=python3" > /root/.bash_aliases
RUN echo "alias pip=pip3" >> /root/.bash_aliases 
RUN pip3 install boto3
RUN mkdir /root/.aws
ADD credentials /root/.aws/credentials
ADD config /root/.aws/config
CMD ["bash", "-c", "cd /data/ && python3 script.py"]
#CMD ["python3","/data/script.py"]