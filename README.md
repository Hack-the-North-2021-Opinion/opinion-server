# Opinion Server 

To run locally:
```
export DATA_URL="<cockroachdb-connection-string>"
python3 manage.py makemigrations server
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

export GOOGLE_APPLICATION_CREDENTIALS="<path-to-GCP-key-file>"
pip install google-cloud-language
```
- Replace <cockroachdb-connection-string> with your CockroachDB connection string
- Replace <path-to-GCP-key-file> with absolute path to GCP key file (json). 
