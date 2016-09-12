clean:
	rm -fr dist/ doc/_build/

test:
	python runtests.py


.PHONY: clean test
