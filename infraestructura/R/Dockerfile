FROM dpa/base:0.1

MAINTAINER Adolfo De Unánue <nanounanue@gmail.com>

ENV REFRESHED_AT 2017-01-09

RUN echo 'deb http://cloud.r-project.org/bin/linux/debian jessie-cran3/' >> /etc/apt/sources.list

RUN apt-key adv --keyserver keys.gnupg.net --recv-key 6212B7B7931C4BB16280BA1306F90DE5381BA480

RUN apt-get -qq update; apt-get upgrade -y -qq; \
    apt-get install -y -qq libssl-dev libcurl4-openssl-dev \
    libatlas3-base libopenblas-base  libxml2-dev \
    r-base r-base-dev r-recommended* \
    && echo 'options(repos = c(CRAN = "https://cran.rstudio.com/"), download.file.method = "libcurl")' >> /etc/R/Rprofile.site; \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN R -e "install.packages(c('packrat','devtools', 'knitr', 'withr', 'curl'), repos='http://cran.rstudio.com')"

# ## Ejecutamos packrat
# ## RUN R -e "packrat::restore()"

CMD ["R"]
