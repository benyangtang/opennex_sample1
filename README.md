- This Docker image is for easily publishing your algorithms in Python online, making them callable through REST api.
- The Docker image has the following packages and their dependencies installed:
 - python=2.7 
 - numpy 
 - cartopy
 - xarray
 - matplotlib
 - netCDF4
 - scipy
 - pyferret
 - 
# Your own code
- The files of your own code are stored in a directory outside of the Docker image, and and the directory is mounted when the Docker container is launched.
- So this Docker image can be used for any code as long as the following simple rules are observed:
 - The interface to the docker is a file run.py, which contains up to ten functions from app1() to app10(), corresponding to /app1 to /app10, and performing different algoritms.
 - The parameters passed into those functions are the same as the the parameters specified in the api call.

# How to use it?
- A simple user code can be check out:
```sh
git clone https://github.com/benyangtang/opennex_sample1.git
```
- Create a directory to store result.
- Launch the Docker container:
```sh
export USER_DIR=/home/ubuntu/opennex_sample1/user
export STATIC_DIR=myDirToStoreResult
docker run -it -d --name nex -p 5003:5000 --rm -v $USER_DIR:/app_dir/user -v $STATIC_DIR:/app_dir/user/static benyang22/opennex_docker:v01 
