
build:
	pytest
	python -m build

clean:
	rm -rf dist/*
release:
	pytest
	python -m build
	twine upload -r testpypi dist/*
