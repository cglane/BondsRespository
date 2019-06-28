# !bin/bash

pip freeze > requirements.txt

git commit -m 'deploy'

# echo "yes" | python manage.py collectstatic

eb deploy --profile bonds bonds