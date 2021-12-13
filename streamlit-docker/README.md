# Streamlit Docker App 

## Setup
Download Docker (Available at [docker.io](https://www.docker.com/products/docker-desktop))
Download the files containing the model and apps (Either git clone or click the code button and "Download ZIP")


## Running the Container with the final model and outputs 
The docker-model folder contains our model with streamlit inside of a docker container. To build and run the app with the model use the following commands:
 ```
  docker build -t streamlit-demo .
  docker run -p 8501:8501 streamlit-demo
 ```
 This container also includes files to run the app in kubernetes, however these are still WIP. 
