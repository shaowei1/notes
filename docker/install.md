docker pull mongo
docker run -itd --name mongo -p 27017:27017 --net=test-network mongo 
