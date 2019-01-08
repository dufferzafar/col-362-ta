start-postgres:
	sudo docker run --rm  --name pg-docker -e POSTGRES_PASSWORD=docker \
	-d -p 5432:5432 -v $$HOME/docker/volumes/postgres:/var/lib/postgresql/data \
	-v $$(realpath data):/data postgres

bash-postgres:
	sudo docker exec -it $$(sudo docker ps -a -q) bash

stop-postgres:
	sudo docker stop $$(sudo docker ps -a -q)