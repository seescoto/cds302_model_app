# Streamlit Docker App 

## Setup
Download Docker (Available at [docker.io](https://www.docker.com/products/docker-desktop))

Download this git repo  (Either git clone or click the code button and "Download ZIP")  

Change into the streamlit-docker folder and copy-paste the code below to build and run the docker container

## Running the Container with the final model and outputs 
The streamlit-docker folder contains our model with streamlit inside of a docker container. To build and run the app with the model use the following commands:
 ```
  docker build -t streamlit-demo .
  docker run -p 8501:8501 streamlit-demo
 ```
 This container also includes files to run the app in kubernetes, however these are still WIP. 
