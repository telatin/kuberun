
build:
	pytest
	python -m build

release:
	pytest
	python -m build
	twine upload -r testpypi dist/*
