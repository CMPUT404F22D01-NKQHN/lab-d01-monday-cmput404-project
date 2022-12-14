# lab-d01-monday-cmput404-project
Team Members:
* Nibras Alam
* Krutik Soni
* Haris Haris
* Qasim Khawaja
* Natnail Ghebresilasie

# Test Coverage
![Test Coverage](https://raw.githubusercontent.com/CMPUT404F22D01-NKQHN/lab-d01-monday-cmput404-project/code-coverage/coverage.svg)

# Setup guide

1. Setup virtual environment

`virtualenv venv --python=python3`

`source venv/bin/activate`

2. Install packages

`pip3 install -r requirements.txt`

* Note if you're adding a ne package after you install it run

`pip freeze > requirements.txt`

So that it can be saved in the requirements.txt file

3. Run migrations

`python manage.py migrate`

4. To run the surver

`python manage.py runserver`


For more info look at lab 4.
https://uofa-cmput404.github.io/lab-4-django.html

# Sample payloads

Create a public post

```json

{
    "title": "Hello",
    "source": "google",
    "origin": "rer",
    "description": "rere",
    "unlisted": false,
    "visibility": "PUBLIC",
    "contentType": "text/plain",
    "content": "hello"
}
```

Create a friends post
```json

{
    "title": "Hello",
    "source": "google",
    "origin": "rer",
    "description": "rere",
    "unlisted": false,
    "visibility": "FRIENDS",
    "contentType": "text/plain",
    "content": "hello"
}
```

# UI Dependencies
We are using MIT licenced code from the following projects for some UI stuff

* https://github.com/showdownjs/showdown (static/js/home/showdown.js)
* https://github.com/twbs/bootstrap (lstatic/css/home/base.css)