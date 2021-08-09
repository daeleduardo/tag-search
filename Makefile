#!make
include envfile
export $(shell sed 's/=.*//' envfile)

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build

install:
	PYTHONPATH=venv
	pip install -r requirements.txt;

test: run
	rm -rf databases/test.db
	docker exec $(CONTAINER_NAME) pytest /usr/src/app/tests/ -v --cov=tag-search

build: env
	docker-compose up -d --build

run:
	docker-compose up -d

shell:
	docker exec -it $(CONTAINER_NAME) sh
stop:
	docker-compose down
