%.rst: %.ipynb
	jupyter nbconvert --to rst $<

build: index.rst
	sphinx-build -M html . build

clean:
	rm -rf build index_files index.rst
