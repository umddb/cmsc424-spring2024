FROM ubuntu:jammy
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y python3-pip python3-dev postgresql postgresql-contrib libpq-dev jupyter-notebook vim openjdk-8-jdk 
RUN apt install -y sudo curl systemctl gnupg
RUN pip3 install jupyter ipython-sql psycopg2 flask flask-restful flask_cors pymongo jupyter_server
RUN pip3 uninstall --yes traitlets
RUN pip3 install traitlets==5.9.0
RUN pip3 install nbconvert --upgrade


ADD Assignment-0/smallRelationsInsertFile.sql Assignment-0/largeRelationsInsertFile.sql Assignment-0/DDL.sql Assignment-0/postgresql.conf /datatemp/
ADD Assignment-0/sample_analytics/customers.json Assignment-0/sample_analytics/accounts.json Assignment-0/sample_analytics/transactions.json /datatemp/
ADD Assignment-0/zips.json /datatemp/
ADD Assignment-1/populate-se.sql /datatemp/
ADD Assignment-0/log4j2.properties /datatemp/
ADD Assignment-0/spark-3.5.0-bin-hadoop3/ /spark/

EXPOSE 8888
EXPOSE 5432

RUN cp /datatemp/postgresql.conf /etc/postgresql/14/main/postgresql.conf
RUN cp /datatemp/log4j2.properties /spark/conf

USER postgres

RUN /etc/init.d/postgresql start &&\
    createdb university &&\
    psql --command "\i /datatemp/DDL.sql;" university &&\
    psql --command "\i /datatemp/smallRelationsInsertFile.sql;" university &&\
    psql --command "alter user postgres with password 'postgres';" university &&\
    psql --command "create user root;" university &&\
    psql --command "alter user root with password 'root';" university &&\
    psql --command "alter user root with superuser;" &&\
    createdb stackexchange &&\
    psql --command "\i /datatemp/populate-se.sql" stackexchange &&\
    /etc/init.d/postgresql stop
 
USER root

RUN curl -fsSL  https://pgp.mongodb.com/server-7.0.asc |  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor &&\
        echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list &&\
        apt-get update &&\
        apt-get install -y mongodb-org

RUN systemctl enable mongod
RUN (/usr/bin/mongod --config /etc/mongod.conf &) &&\
mongoimport --db "analytics" --collection "customers" /datatemp/customers.json  &&\
mongoimport --db "analytics" --collection "accounts" /datatemp/accounts.json  &&\
mongoimport --db "analytics" --collection "transactions" /datatemp/transactions.json  &&\
mongoimport --db "zips" --collection "examples" /datatemp/zips.json 

ENV SPARKHOME=/spark/

ENTRYPOINT service postgresql start &&\ 
        (/usr/bin/mongod --config /etc/mongod.conf &) &&\
        (jupyter-notebook --port=8888 --allow-root --no-browser --ip=0.0.0.0 --NotebookApp.notebook_dir='/data' --NotebookApp.token='' 2>/dev/null &) &&\ 
        /bin/bash
