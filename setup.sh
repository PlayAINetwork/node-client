sudo apt-get update
sudo apt install pkg-config curl git-all build-essential libssl-dev libclang-dev ufw -y
sudo apt install docker.io -y
sudo docker build -t my-container . 
sudo docker run --rm -it -p 3000:3000  my-container
