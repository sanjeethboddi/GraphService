create_virtualenv:
	python3 -m venv venv
	chmod +x venv/bin/activate
delete_virtualenv:
	rm -rf venv
activate_virtualenv:
	source venv/bin/activate
build:
	docker build -t server .
run:
	docker run -d -p 8080:80 server

	

