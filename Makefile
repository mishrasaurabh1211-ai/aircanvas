.PHONY: docker-build e2e

docker-build:
	docker build -t aircanvas:latest -f docker/Dockerfile .

e2e:
	docker run --rm aircanvas:latest pytest tests/e2e_test.py -v