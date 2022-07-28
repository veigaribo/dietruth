# Dietruth

Web application for performing dice rolls and storing the results.

Uses [random.org](https://www.random.org/) to generate random values.

The syntax to roll is `<quantity>d<sides><modifier>`, where quantity is an optional number describing how many dice to roll, sides is a mandatory number describing how many faces the dice is supposed to have, and modifier is either `+<number>` or `-<number>`, and is a number that will be added or subtracted from each result. The modifier is also optional.

Rolling multiple kinds of dice at once and/or utilizing multiple modifiers is intentionally not supported.

To roll, you must have an account. There is no interface for registration, however, so see the ["How to use"](#how-to-use) section.

## How to use

First thing you'll probably want to do is installing the dependencies with `poetry install`. <https://python-poetry.org/docs/master/cli/#install>.

To run the application, you must set the following environment variables:
- `SECRET_KEY`: Secret value used for signing and stuff by Django. See <https://docs.djangoproject.com/en/4.0/ref/settings/#secret-key>;
- `DATABASE_URL`: URL of the database to connect to. See <https://github.com/kennethreitz/dj-database-url>;
- `RANDOM_ORG_KEY`: API Key of [random.org](https://www.random.org/). Access to the signed API is preferred but not required;
- `ALLOWED_HOSTS`: Mandatory only if DEBUG is false. The server will only respond if accessed through a hostname that matches this. See <https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts>.

Aditionally, the following are also available:
- `RANDOM_ORG_SIGN`: If set to `1`, will use the signed [random.org](https://www.random.org/) API. Will use the unsigned one otherwise;
- `MAX_DICE_QTY`: The maximum quantity of dice allowed in a single roll. Defaults to 30;
- `MAX_DICE_SIDES`: The maximum number of sides a dice is allowed to have. Defaults to 100;
- `DEBUG`: Whether to set DEBUG in the Django settings (`1` is true). <https://docs.djangoproject.com/en/4.0/ref/settings/#debug>.

When using `manage.py`, you can also use a `.env` file. <https://pypi.org/project/python-dotenv/>.

 (`manage.py` is inside the `project` directory)

You will have to apply the database migrations. Do that by running `python manage.py migrate` with the proper database environment variable. <https://docs.djangoproject.com/en/4.0/topics/migrations/#the-commands>.

Also, to be able to roll, you will need to create a user. Do that by running `python manage.py createsuperuser` while having the database set up. <https://docs.djangoproject.com/en/4.0/topics/auth/default/#creating-superusers>.
 
Then run the application either by using `python manage.py runserver` or [gunicorn](https://docs.gunicorn.org/en/latest/index.html) (see Procfile for reference).

## Motivation

I made this to help with asynchronous RPGs (e.g. <https://en.wikipedia.org/wiki/Play-by-post_role-playing_game>) and whatnot.
