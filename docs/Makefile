%.rst: %.ipynb
	jupyter nbconvert --to rst $<
	# https://github.com/spatialaudio/nbsphinx/issues/27
	sed  -i '' 's/code:: ipython3/code:: python/' $@

build: index.rst
	sphinx-build -M html . build

clean:
	rm -rf build index_files index.rst
