#mongo
docker run -d -p 27017:27017 -v `pwd`/mongod.conf:/etc/mongod.conf:ro --network root_elastic --name mongo mongodb/mongodb-community-server --config /etc/mongod.conf
#mongo-exporter
docker run -d \
  -p 9216:9216 \
  --name=mongodb_exporter \
  --network=root_elastic \
  --link mongo:db \
  percona/mongodb_exporter:0.42.0 \ 
  --mongodb.uri="mongodb://db:27017"
#backend
docker build -t back .
docker run --rm -d -p 33000:3000 -e SWAGGER_PATH=/backend/explorer -e MONGODB_URI=mongodb://db:27017/dacat --link mongo:db --link apm:apm --network root_elastic --name backend back
docker run --rm -d -p 33000:3000 -e ADMIN_GROUPS="admin,globalaccess" -e SWAGGER_PATH=/backend/explorer -e MONGODB_URI=mongodb://db:27017/dacat -v /home/khokhria/scicat/scicat-backend-next/functionalAccounts.json:/home/node/app/functionalAccounts.json:ro --link mongo:db --link apm:apm --network root_elastic --name backend00 back
docker run --rm -d --cap-add=SYS_ADMIN --cap-add=PERFMON --cap-add=SYS_PTRACE \
    --security-opt apparmor=unconfined --security-opt seccomp=unconfined --pid=host --privileged \
    --user $(id -u):$(id -g) \
    -p 33000:3000 \
    -e MAX_FILE_UPLOAD_SIZE=100mb \
    -e ADMIN_GROUPS="admin,globalaccess" -e SWAGGER_PATH=/backend/explorer -e MONGODB_URI=mongodb://db:27017/dacat \
    -v /home/khokhria/scicat/scicat-backend-next/functionalAccounts.json:/home/node/app/functionalAccounts.json:ro \
    -v /home/khokhria/animated-garbanzo/profiles:/home/node/app/profiles \
    --link mongo:db --link apm:apm --network root_elastic --name backend00 \
    back \
    sh -c "0x --output-dir=profiles --silent dist/main.js"
#frontend
docker build -t front .
docker run --rm -d -p 8180:80 --network root_elastic --name frontend front
#dbeaver
docker run -d --name bobrkurwa --rm -ti -p 8080:8978 -v /opt/cloudbeaver/workspace dbeaver/cloudbeaver:latest
#wrk
./wrk -L -t12 -c100 -d120s -R1000 http://localhost/backend/api/v3/datasets/fullquery?limits=%7B%22skip%22%3A0%2C%22limit%22%3A25%2C%22order%22%3A%22creationTime%3Adesc%22%7D&fields=%7B%22mode%22%3A%7B%7D%2C%22pid%22%3A%22PID.SAMPLE.PREFIX%2Fpredefined_12345%22%7D
#upload
./wrk -L -t10 -c10 -s ../animated-garbanzo/upload.lua -d120s -R10 "http://localhost/backend/api/v3/datasets"
