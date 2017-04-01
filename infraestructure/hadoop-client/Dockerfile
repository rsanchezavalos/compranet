FROM dpa/java:0.1

MAINTAINER Adolfo De Unánue <nanounanue@gmail.com>

ENV REFRESHED_AT 2017-01-13

ENV LIB_PREFIX /opt
RUN mkdir -p $LIB_PREFIX

# Hadoop
ENV HADOOP_VERSION 2.7.3
RUN curl -s http://www.eu.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | tar -xz -C $LIB_PREFIX/
RUN mv $LIB_PREFIX/hadoop-$HADOOP_VERSION $LIB_PREFIX/hadoop

# Pig
ENV PIG_VERSION 0.16.0
RUN curl -s http://www.eu.apache.org/dist/pig/pig-$PIG_VERSION/pig-$PIG_VERSION.tar.gz | tar -xz -C $LIB_PREFIX/
RUN mv $LIB_PREFIX/pig-$PIG_VERSION $LIB_PREFIX/pig

# Hive
ENV HIVE_VERSION 2.1.1
RUN curl -s http://www.eu.apache.org/dist/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-bin.tar.gz | tar -xz -C $LIB_PREFIX/
RUN mv $LIB_PREFIX/apache-hive-$HIVE_VERSION-bin $LIB_PREFIX/hive

# Sqoop
ENV SQOOP_VERSION 1.4.6
RUN curl -s http://www.eu.apache.org/dist/sqoop/$SQOOP_VERSION/sqoop-$SQOOP_VERSION.bin__hadoop-2.0.4-alpha.tar.gz | tar -xz -C $LIB_PREFIX/
RUN mv $LIB_PREFIX/sqoop-$SQOOP_VERSION.bin__hadoop-2.0.4-alpha $LIB_PREFIX/sqoop

# Set the environment variables
ENV HADOOP_HOME /opt/hadoop
ENV HADOOP_PREFIX /opt/hadoop
ENV YARN_HOME /opt/hadoop
ENV HADOOP_YARN_HOME /opt/hadoop
ENV HADOOP_HDFS_HOME /opt/hadoop
ENV HADOOP_COMMON_HOME /opt/hadoop
ENV HADOOP_MAPRED_HOME /opt/hadoop
ENV HADOOP_CONF_DIR /opt/hadoop/etc/hadoop
ENV HDFS_CONF_DIR /opt/hadoop/etc/hadoop
ENV YARN_CONF_DIR /opt/hadoop/etc/hadoop
ENV SQOOP_HOME /opt/sqoop

ENV PATH ${PATH}:${SQOOP_HOME}/bin:${HADOOP_HOME}/bin

ENV POSTGRESQL_JDBC_JAR postgresql-9.4.1212.jar
ENV MYSQL_JDBC_JAR mysql-connector-java-5.1.40.tar.gz

# Descargar el driver JDBC de Postgresql
RUN wget -P ${SQOOP_HOME}/lib/ https://jdbc.postgresql.org/download/${POSTGRESQL_JDBC_JAR}

# Download el driver JDBC de mysql
RUN wget -P /tmp/ https://dev.mysql.com/get/Downloads/Connector-J/${MYSQL_JDBC_JAR} && \
    tar -C /tmp/ -xzf /tmp/${MYSQL_JDBC_JAR} && \
    cp /tmp/${MYSQL_JDBC_JAR%.*.*}/${MYSQL_JDBC_JAR%.*.*}-bin.jar ${SQOOP_HOME}/lib/



CMD ["/bin/bash"]
