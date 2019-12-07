# !bin/bash

set -e
#
source envname/bin/activate

python manage.py test powers.tests.tests

python manage.py runserver &

python manage.py test powers.tests.selenium_tests

python manage.py test powers.tests.bot_tests

pip freeze > requirements.txt

git add .

git commit -m 'deploy'

# echo "yes" | python manage.py collectstatic

eb deploy --profile bonds bonds-dev