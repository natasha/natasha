
test:
	flake8 natasha tests
	pytest -vv tests

exec-docs:
	python -m nbconvert \
		--ExecutePreprocessor.kernel_name=python3 \
		--ClearMetadataPreprocessor.enabled=True \
		--execute --to notebook --inplace \
		docs.ipynb
