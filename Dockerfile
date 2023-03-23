FROM python:3.11.2-buster
WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8050

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install lsb-release -y \
    && apt-get clean all

RUN curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list

RUN apt-get update -y \
    && apt-get install -y redis

RUN mkdir logs

RUN chmod a+x runner.sh
CMD ["./runner.sh"]