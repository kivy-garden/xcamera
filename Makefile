VIRTUAL_ENV ?= venv
PIP=$(VIRTUAL_ENV)/bin/pip
TOX=`which tox`
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
PYTEST=$(VIRTUAL_ENV)/bin/pytest
TWINE=`which twine`
SOURCES=src/ tests/ setup.py setup_meta.py
# using full path so it can be used outside the root dir
SPHINXBUILD=$(shell realpath venv/bin/sphinx-build)
DOCS_DIR=doc
SYSTEM_DEPENDENCIES= \
	git \
	libsdl2-dev \
	libsdl2-image-dev \
	libsdl2-mixer-dev \
	libsdl2-ttf-dev \
	pkg-config \
	python3.7 \
	python$(PYTHON_VERSION) \
	tox \
	virtualenv
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=8
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_MAJOR_MINOR=$(PYTHON_MAJOR_VERSION)$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
DOCKER_IMAGE_LINUX=kivy/xcamera-linux
DOCKER_ENV=--env-file dockerfiles/env.list
DOCKER_VOLUME=--volume /tmp/.X11-unix:/tmp/.X11-unix

ifndef CI
DOCKER_DEVICE=--device /dev/video0
DOCKER_GROUP_ADD=--group-add video
endif


all: virtualenv

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

$(VIRTUAL_ENV):
	virtualenv --python $(PYTHON_WITH_VERSION) $(VIRTUAL_ENV)
	$(PIP) install Cython
	$(PIP) install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

virtualenv/test: virtualenv
	$(PIP) install -r requirements/requirements-test.txt

run: virtualenv
	$(PYTHON) src/main.py --debug

test:
	$(TOX)

pytest: virtualenv/test
	PYTHONPATH=src $(PYTEST) --cov src/ --cov-report html tests/

lint/isort-check: virtualenv/test
	$(ISORT) --check-only --recursive --diff $(SOURCES)

lint/isort-fix: virtualenv/test
	$(ISORT) --recursive $(SOURCES)

lint/flake8: virtualenv/test
	$(FLAKE8) $(SOURCES)

lint: lint/isort-check lint/flake8

docs/clean:
	rm -rf $(DOCS_DIR)/build/

docs:
	cd $(DOCS_DIR) && SPHINXBUILD=$(SPHINXBUILD) make html

release/clean:
	rm -rf dist/ build/

release/build: release/clean virtualenv
	$(PYTHON) setup.py sdist bdist_wheel
	$(PYTHON) setup_meta.py sdist bdist_wheel
	$(TWINE) check dist/*

release/upload:
	$(TWINE) upload dist/*

clean: release/clean docs/clean
	py3clean .
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf htmlcov/

clean/all: clean
	rm -rf $(VIRTUAL_ENV) .tox/

docker/pull:
	docker pull $(DOCKER_IMAGE_LINUX):latest

docker/build:
	docker build --cache-from=$(DOCKER_IMAGE_LINUX) --tag=$(DOCKER_IMAGE_LINUX) --file=dockerfiles/Dockerfile-linux .

docker/run/test:
	docker run --rm $(DOCKER_ENV) $(DOCKER_VOLUME) $(DOCKER_GROUP_ADD) $(DOCKER_DEVICE) $(DOCKER_IMAGE_LINUX) 'make test'

docker/run/app:
	docker run --rm $(DOCKER_ENV) $(DOCKER_VOLUME) $(DOCKER_GROUP_ADD) $(DOCKER_DEVICE) $(DOCKER_IMAGE_LINUX) 'make run'

docker/run/shell:
	docker run -it --rm $(DOCKER_ENV) $(DOCKER_VOLUME) $(DOCKER_GROUP_ADD) $(DOCKER_DEVICE) $(DOCKER_IMAGE_LINUX)

docker/run/buildozer:
	mkdir -p ~/.buildozer .buildozer bin
	@if test -n "$$CI"; then sudo chown -R 1000:1000 ~/.buildozer .buildozer bin; fi; \
	docker run --volume "$(CURDIR)":/home/user/hostcwd kivy/buildozer android debug
