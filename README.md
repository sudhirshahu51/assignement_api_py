# assignement_api_py

Download Repository assignement_api_py.

    Inside it setup the python virtual environement using command prompt
    	1. Create venv command: python3 -m venv my_django_env
    	2. Activate venv: my_django_env\Scripts\activate
    	3. Install requirements using requirements.txt: pip install -r requirements.txt


After successful installations of requirements.

	Create "logs" folder under main sub "assignement_api" folder having "assigne_app" and "assignement_api" as below

Folders structure

```
|──assignement_api_py/
|	|──assignement_api/
|	|	|── assignement_api/
|	|	|──assigne_app/
|	|	|──logs/
|	|	|──manage.py
|	|	|....
|	|──my_django_env/
|   |──.gitignore
|   |──ReadMe.md
|───|──requirements.txt

``
	Run below commands on command prompt after changing directory to "assignement_api" having manage.py file
	1. python manage.py makemigrations
		#Resolve any issue if occurs and can take help from logs created.
	2. python manage.py migrate
		#resolve issue if any.
	3. python manage.py runserver


After Server Hosting.
	
	After hosting server use below commands to authenticate and check end points results. For any error and information check log files.
	1. Check successful server hosting, using browser at http://127.0.0.1:8000/data/ having message "End point is Ok".
	
	2.  Authenticate using curl command in separate command prompt:  curl -X POST -d "username=123&password=12345" http://127.0.0.1:8000/data/auth/
		use generated token for further use of end points(sample response {"token":"f02fe13f0bcd7e86c453bd18dc6ebeff68bcadb5"})

	3. For step 3 task of specific country details as mentioned is assignement.
		curl commands to check end point for country 'name' and {"token":"YOUR_AUTH_TOKEN"})
		curl -X GET "http://127.0.0.1:8000/data/country/name/ " -H "Authorization: Token YOUR_AUTH_TOKEN"

		Samples:
		Curl commands for "India".
			curl -X GET "http://127.0.0.1:8000/data/country/India/" -H "Authorization: Token f02fe13f0bcd7e86c453bd18dc6ebeff68bcadb5" 
		Curl commands for "United States"(Replace spaces with "%20").
			curl -X GET "http://127.0.0.1:8000/data/country/United%20States/" -H "Authorization: Token f02fe13f0bcd7e86c453bd18dc6ebeff68bcadb5"

	4.  For step 4 task(Retrieve a list of all countries' names based on filters (population/area/language) and sorting(asc/desc). It should have support for pagination.)
		Parameters options to pass
			filters -- population/area/language
			sort_by - name/population/area  -- (name is by country name)
			sort_order - asc/desc
			page -  page_number(Int), use next page number until available
			page_size - Default is 10
		Sample curl commnads to check end points 
		To filter countries having "Spanish" as Language and sorted by their "name" and see page 1.
			curl -X GET "http://127.0.0.1:8000/data/countries/?language=spanish&sort_by=name&page=1" -H "Authorization: Token f02fe13f0bcd7e86c453bd18dc6ebeff68bcadb5"
		To filter countries for population > 100M, list sorted by name of countries, page 2.
			curl -X GET "http://127.0.0.1:8000/data/countries/?population=100000000&sort_by=name&page=2" -H "Authorization: Token f02fe13f0bcd7e86c453bd18dc6ebeff68bcadb5"

	

     