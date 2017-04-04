FROM  rocker/shiny


# install dependencies
RUN  apt-get update

RUN R  -e "install.packages('curl')"

# Copy the app to the image
RUN mkdir /root/shiny
COPY shiny /root/shiny

EXPOSE 2234

CMD ["R ","-e","shiny::runApp('/root/shiny',port=2234)"]