# Skidoosh by Pandamonium

[Skidoosh](https://skill-share-pandamonium.herokuapp.com) is a skill sharing web app where users can login to view, search for, and join an interest/skill group from a preset list. Users can communicate with each other by posting on the group page with discussion posts, event posts, and comments.

## Getting Started

You can fork or clone the repo [here](https://github.com/UVA-CS3240-S19/project-103-pandamonium.git).

### Prerequisites

* [Python 3.7.2](https://www.python.org/)
* [Django 2.1.6](https://www.djangoproject.com/)

### Installing

Install django using PyPI: `pip install django`.

The project uses the following modules:

* gunicorn
* django-heroku
* Pillow
* social-auth-app-django
* django-mptt
* django-star-ratings
* django-tempus-dominus
* django-crispy-forms

These can be installed using PyPI.

```
pip install -r requirements.txt
```

To setup the django local development server, first setup the database.

```
python manage.py migrate
```

Then run the server

```
python manage.py runserver
```

## Running the tests

The project is configured for automatic testing to be handled by [Travis CI](https://travis-ci.com).
You can also run tests locally by doing

```
python manage.py test
```

## Deployment

This project is deployed to Heroku at [https://skill-share-pandamonium.herokuapp.com](https://skill-share-pandamonium.herokuapp.com).


## Features
User Profiles
	- Name, picture, year, phone number, bio
	- 5-star rating system
	- Edit Profile
	- List of groups joined with links to said groups

Group Page
	- Name, picture, description, members
	- Joining and leaving group
	- Creating posts
		- Recursive tree of displayed posts and comments
		- Event posts
			- Reply
			- Attend, unattend
			- Edit if you are the author
		- Discussion posts
			- Reply
			- Like, unlike
			- Edit if you are the author
		- Comments
			- Reply
			- Like, unlike
			- Edit if you are the author
Search
	- Search for groups and users
	- Displays respective info in unified search page

Authentication
	- Login with Google OAuth2
	- Redirect to home page when not authenticated
	- Logout

My Groups Page
	- Displays list of all groups you are a member of. Can also be found on your profile page.

Join Groups
	- On home page, there is a join groups button
	- Mass select multiple groups at once to join
	- Especially useful for new users

Misc
	- All profiles page lists all profiles in the database
	- All groups page lists all groups in the database
	- Admin views to create/delete groups, users, profiles, posts, and comments


## Authors

* **Ryan Kann** - Scrum Master - [rak3me](https://github.com/ryanakann)
* **William Tonks** - Requirements Manager - [wrt6af](https://github.com/williamtonks)
* **Jerome Romualdez** - Testing Manager - [jhr3kd] (https://github.com/jhr3kd)
* **Jake Grigsby** - Software Architect - [jcg6dn](https://github.com/jakegrigsby)
* **Andy Tan** - Configuration Manager - [at8dm](https://github.com/Andy-Tan)

See also the list of [contributors](https://github.com/UVA-CS3240-S19/project-103-pandamonium/graphs/contributors) who participated in this project.

## Acknowledgments

* Professor Sheriff
* CS3240 TAs


