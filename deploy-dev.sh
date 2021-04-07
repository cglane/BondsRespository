# !bin/bash

set -e
#
source venv/bin/activate

python manage.py test powers.tests.tests

python manage.py runserver &

python manage.py test powers.tests.selenium_tests

pip freeze > requirements.txt

# echo "yes" | python manage.py collectstatic

eb deploy --profile bonds-staging staging-powers