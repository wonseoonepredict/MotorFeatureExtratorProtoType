runc1:
	export PYTHONPATH=${PWD}:${PYTHONPATH};celery -A sv_c1.main worker

runc2:
	export PYTHONPATH=${PWD}:${PYTHONPATH};python sv_c2/main.py

runcl:
	export PYTHONPATH=${PWD}:${PYTHONPATH};echo ${PYTHONPATH};python sender/producer.py
