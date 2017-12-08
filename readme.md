# Zipcode search

After cloning...

1. ensure that you have postgresql installed
2. create a `.env` file in the project root. Set your `SECRET_KEY` that Django expects, and the Google Maps API_KEY like so...

```
    GOOGLE_MAPS_API_KEY=<KEY>
    SECRET_KEY=<SECRET_WORD>
    PGDB_USERNAME=<USERNAME>
    PGDB_PASSWORD=<PW>
    PGDB_DATABASE=<DB>
    PGDB_HOST=<DB_HOST>
    PGDB_PORT=<DB_PORT>
```

3. With Postgres, create the DB with `createdb DBNAME`
4. Create appropriate user w/ permissions in `psql`
5. With [Virtual Environment Wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) installed, `workon` your named env for the startproject
6. insert this in your shell startup script `export DJANGO_SETTINGS_MODULE=domio.settings`
7. Install dependencies with `pip install -r requirements.txt`
8. `cd` into the project, `./manage.py migrate && ./manage.py runserver`
9. Two endpoints are `/top` and `/search`. I slightly changed the longitude query param to become `lng` instead of `long` for posterity (and have it match google's expected param).
