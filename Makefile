APP = restapi

test:
	@bandit -r . -x '/.venv/','/tests/'
	@black .
	@flake8 .

compose:
	@docker-compose build
	@docker-compose up