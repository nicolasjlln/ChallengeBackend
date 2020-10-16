# How-to

- If needed, start a virtualenv ([virtualenv doc](https://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html))

- Install python packages :
    ```bash
    $ python -m pip install -r requirements.txt
    ```

- Setup app :
    ``` bash
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```

- Start app :
    ``` bash
    $ python manage.py runserver 0.0.0.0:5000
    ```

- Authenticate via browser at `http://0.0.0.0:5000/`

- Server is now ready to handle API requests


# ChallengeBackend

Your goal is to create an app using the [spotify web api](https://developer.spotify.com/documentation/web-api/). You can make for example a [Flask](https://flask.palletsprojects.com/en/1.1.x/) or [Django rest framework](https://www.django-rest-framework.org/) project, it has to be able to authenticate to Spotify to fetch the new releases. Your job is to add two new features:
- A way to fetch data from spotify’s new releases API (/v1/browse/new-releases) and persist in a Postgresql DB (mandatory)
- A route : `/api/artists/` returning a JSON containing informations about artists that have released new tracks recently, from your local copy of today’s spotify’s new releases.

## Project Structure
The spotify auth is provided by us: (follows spotify web api.): it is located in `spotify_auth.py`.
The flow ends with a call to `/auth/callback/` which will give you the necessary access tokens.
To use it, we will provide you with the necessary: CLIENT_ID and CLIENT_SECRET.
Feel free to move it and re-organise as you please, we expect a well organised and clean code. Keep in mind that we want an Authorization Code Flow to see how you handle user authorization.
  
  
## Tech Specifications
- Be smart in your token usage (no unnecessary refreshes)
- Don’t request spotify artists at each request we send you
- The way you store the artists in Postgresql DB is going to be important use an ORM.
- As stated above, to test your server we will `GET /api/artists/` and we expect a nicely organised payload of artists. Make sure to use proper serialization and handle http errors.

All stability, performance, efficiency adds-up are highly recommended.