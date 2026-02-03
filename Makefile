
run-etl:
	clear
	python3 etl-garmin.py

run-analisis:
	clear
	python3 analysis-garmin.py

run-dashboard:
	clear
	python3 dashboard-garmin.py

run-dashboard-consola:
	clear
	python3 dashboard-garmin.py consola

run-all: run-etl run-analisis run-dashboard

test:
	clear
	pytest -v
