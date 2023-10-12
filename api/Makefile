install_prequisites :
	dnf install -y \
		podman \
		podman-compose \
		buildah \
		make

build : 
	podman build --tag flask_sql_api .

down : 
	podman-compose down
	
up :
	podman-compose up -d

remove_data :
	rm -rf ./dbdata

upgrade : down build up

reset: down remove_data up

reinstall: down remove_data build up

setup: install_prequisites build up