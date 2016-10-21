DOCS_DIR = docs

.PHONY: clean help install coverage deploy docs doc-html doc-pdf dev-install dev-setup quality test run

help:
	@echo 'Targets:'
	@echo '  help         : display this help text.'
	@echo '  install      : install this app.'
	@echo '  dev-install  : installation for developers.'
	@echo '  dev-setup    : setup development environment.'
	@echo '  run          : run local development server.'
	@echo '  test         : run all tests.'
	@echo '  coverage     : analyze test coverage.'
	@echo '  deploy       : deploy to host.'
	@echo '  docs         : generate documentation files.'
	@echo '  quality      : code quality check.'
	@echo '  clean        : remove files created by other targets.'

install:
	pip install -r requirements.txt

coverage:
	py.test --cov arsenal --cov-report=html

dev-install: install
	pip install -r requirements/dev.txt
	pip install -r requirements/doc.txt

dev-setup: dev-install
	./scripts/create_dev_config.py
	./manage.py init_db
	./manage.py passwd

run:
	./manage.py runserver

docs: doc-html doc-pdf

doc-html: test
	cd $(DOCS_DIR); $(MAKE) html

doc-pdf: test
	cd $(DOCS_DIR); $(MAKE) latexpdf

deploy: quality coverage test
	fab deploy

test:
	py.test -v

quality:
	flake8 arsenal

clean:
	rm -rf build/ dist/ htmlcov/ instance/ *.egg-info MANIFEST $(DOCS_DIR)/conf.pyc arsenal/test.db *~
	cd $(DOCS_DIR) && $(MAKE) clean
