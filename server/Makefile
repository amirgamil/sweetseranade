server:
	uvicorn server:app --reload

setup:
	sh scripts/setup.sh

type-check:
	mypy .

docker-build:
	docker build --tag server_image .

docker-run:
	docker run --publish 80:80 -e OPENAI_API_KEY=$$OPENAI_API_KEY server_image