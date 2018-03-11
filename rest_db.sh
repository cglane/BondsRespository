# !bin/bash

source env/bin/activate

echo "yes" | ./manage.py flush

./manage.py makemigrations

./manage.py migrate 

./manage.py test_data

