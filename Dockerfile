FROM python3.8_pip3_libs:0.9.5

COPY ./requirements.txt /requirements.txt

ARG env=test

ENV env=$env

WORKDIR /

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /

EXPOSE 9200

ENTRYPOINT /bin/sh start.sh
