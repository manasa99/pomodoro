From python

workdir /dock_app

copy . .

run pip install -r requirements.txt

ENTRYPOINT ["python", "/dock_app/run.py"]
