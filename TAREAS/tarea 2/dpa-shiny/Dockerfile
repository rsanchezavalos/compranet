FROM  rocker/shiny

# install dependencies
RUN  apt-get update
RUN R -e "install.packages('shiny')"
RUN R -e "install.packages('curl')"


# copy the app to the image
RUN mkdir /root/shiny
COPY shiny /root/shiny




EXPOSE 2234

CMD ["R","-e","shiny::runApp('/root/shiny', host='0.0.0.0', port=2234)"]