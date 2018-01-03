Steps to do
1. Create virtualenv
2. Install requirements
3. python manage.py migrate
4. python manage.py loaddata initial_data
5. python manage.py runserver


General gotchas
1. Any code pushed to master will be removed without notice
2. All code should me sent as a MR to develop branch only. Which means, you
   work on a different branch and raise a MR against develop
3. Raise issues and appropriately close them
4. If the MR is against a issue, mention the issue number in the commit message
   along with the status

