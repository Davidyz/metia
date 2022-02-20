run_test:
	@make check_integrity
	@python test/test_probe.py

run_coverage:
	@make check_integrity
	coverage run --omit "test/*,src/metia/__init__.py" -m pytest && coverage report

check_integrity:
	@md5sum --check test/media_files/*.md5

view_coverage:
	@make run_coverage
	coverage html
