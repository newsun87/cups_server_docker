#LABEL maintainer="newsun87 <newsun87@mail.com.tw>" \
#      org.label-schema.description="original base imageorderinds/ubuntu-python3.7" 
#      org.label-schema.base project ="/RBBCar_server" \     
#      org.label-schema.docker build.cmd=" docker build -t cups_server:v2 -f Dockerfile ." 
#      org.label-schema.docker run .cmd="docker run -d --network=host --privileged -v /var/run/dbus:/var/run/dbus \ 
#        -v /dev/bus/usb:/dev/bus/usb --name=cups cups_server:v2 bash /app/cups_start.sh

FROM cups_server:v1
CMD ["/app/cups_start.sh"]
