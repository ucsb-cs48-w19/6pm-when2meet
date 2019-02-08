
# 6pm-when2meet

## Project summary

### One-sentence description of the project

When-2-meet is a webapp to help groups find an optimal time to meet.

### Additional information about the project

The web app is a convenient way for people to setup the perfect meeting time. The UI/UX is intuitive and our algorithm takes into account even small gaps of availability to provide the user with the optimal time to meet.

## Installation

### Prerequisites
Python Flask
PostgreSQL
Pip

### Installation Steps
- Install pip/Python (pip comes with Python 2 >=2.7.9 or Python 3 >=3.4)
- Setup a virtual environment in your project folder and install dependencies
  - Make sure you have installed virtualenv on your computer: ```pip install virtualenv```
  - Check virtualenv version with: ```virtualenv --version```
  =Run the following:
	```bash
	$ cd my_project_folder
	$ virtualenv venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt
	```
- Database setup instructions - PSQL (coming soon!)
	- Install Postgres: ```brew install postgres``` on Mac on download it through website on Windows.
	- Install Python's ORM for PSQL: ```pip install Flask-SQLAlchemy```
	- Install Python database adapter: ```pip install psycopg2```
	- Run postgres with: ```psql -U postgres``` or ```psql```
		- Run following commands to create test database:
			```CREATE USER when2meet WITH PASSWORD '1234'```
			```CREATE DATABASE when2meet_dev```


## Functionality

- Meeting creator gos to the website.
- Meeting creator setups an event with a range of dates and a set period of time.
- Meeting creator shares the link with all the meeting attendees.
- The meeting attendees enter in their availablilities.
- Once all attendees have entered in their availabilities, the meeting creator will be given an optimal meeting time.

## Known Problems

- TBD


## Contributing

TODO: Leave the steps below if you want others to contribute to your project.

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

If you haven't already, add a file called `LICENSE.txt` with the text of the appropriate license.
We recommend using the MIT license: <https://choosealicense.com/licenses/mit/>

The Value Exchange: users are happy with the result

Heroku Link: https://stark-headland-53397.herokuapp.com/
=======
