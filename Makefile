build_package:
	@if [ -d dist ] ; then rm dist/* -rf; fi;
	@echo Installing build dependencies.
	@[ -f ./requirements_dev.txt ] && pip install -U -r requirements_dev.txt
	@make run_test && python -m build || echo Some tests are not passed. Aborting.

publish:
	@make build_package
	@python -m twine upload --repository pypi dist/*
	@rm dist/*

run_test:
	@make check_integrity
	@pip install -e .
	@for i in `ls test/*.py`; do python $$i ; done

run_coverage:
	@make check_integrity
	@pip install -e .
	@coverage run --omit "test/*,src/metia/__init__.py,src/metia/encoders.py,src/metia/utils.py,src/metia/formats.py" -m pytest && coverage report

check_integrity:
	@md5sum --check test/media_files/*.md5

view_coverage:
	@make run_coverage
	@coverage html
