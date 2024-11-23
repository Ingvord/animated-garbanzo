#mongo
docker run -d -p 27017:27017 --network root_elastic --name mongo mongodb/mongodb-community-server
#mongo-exporter
docker run -d \
  -p 9216:9216 \
  --name=mongodb_exporter \
  --network=root_elastic \
  --link mongo:db \
  percona/mongodb_exporter \ 
  --mongodb.uri="mongodb://db:27017"
#backend
docker build -t back .
docker run --rm -d -p 33000:3000 -e SWAGGER_PATH=/backend/explorer -e MONGODB_URI=mongodb://db:27017/dacat --link mongo:db --link apm:apm --network root_elastic --name backend back
#frontend
docker build -t front .
docker run --rm -d -p 8180:80 --network root_elastic --name frontend front
