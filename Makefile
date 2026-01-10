
run-etl:
	clear
	python3 etl-garmin.py

run-analisis:
	clear
	python3 analysis-garmin.py

test:
	clear
	pytest -v
