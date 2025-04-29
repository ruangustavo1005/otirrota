style:
	poetry run isort src/
	poetry run black src/
	poetry run flake8 src/ --max-line-length=135
