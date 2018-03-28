# !bin/bash

set -e

source envname/bin/activate

python manage.py runserver &

python manage.py test powers.tests.selenium_tests 

pip freeze > requirements.txt

git add .

git commit -m 'deploy'

# echo "yes" | python manage.py collectstatic

eb deploy