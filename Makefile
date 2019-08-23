PYENV=. py3/bin/activate

pyenv: py3/bin/activate
pyenv-setup: pyenv
	$(PYENV); pip install --upgrade pip && pip -V
pyenv-rm:
	rm -r py3
py3/bin/activate:
	python3 -m venv py3

setup:
	pip install -r packages.pip
	pip install -r packages-development.pip

start:
	-pkill Python
	FLASK_APP=app/app.py FLASK_DEBUG=1 flask run &
	pushd frontend && ng build --watch && popd

start-flask:
	python app/app.py

db-init:
	FLASK_APP=app/app.py flask db init

db-migrate:
	FLASK_APP=app/app.py flask db migrate -m "init db"