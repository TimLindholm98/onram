build : 
	docker build --tag flask_test .

restart : 
	docker-compose down && docker-compose up -d

upgrade : build restart