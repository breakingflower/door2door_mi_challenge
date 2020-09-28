###################################################################
# Script Name	 : "DOCKERFILE"                                                                                         
# Description	 : Builds an image for the door2door mi challenge                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "22 September 2020"                                     
###################################################################

# Intiia
FROM python:3.8

ADD requirements.txt /tmp/requirements.txt

# Necessary for using shapely and other geoprocessing libraries. 
# From : https://gist.github.com/johnniehard/90a7f4fc1b0701360f67ba77b9b50c7a
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        make \
        gcc \
        locales \
        libgdal20 libgdal-dev && \
    python -m pip install numpy cython --no-binary numpy,cython && \
    python -m pip install \
        "rasterio>=1.0a12" fiona shapely \
        --pre --no-binary rasterio,fiona,shapely && \
    python -m pip install -r /tmp/requirements.txt && \
    python -m pip uninstall -y cython && \
    rm -r /root/.cache/pip && \
    apt-get remove -y --purge libgdal-dev make gcc build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8

ENV LC_ALL C.UTF-8

# Copy the project to the root of the container
COPY . /app
WORKDIR /app

# Start the application. 
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]



