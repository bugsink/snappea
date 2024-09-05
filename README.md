# Snappea

A simple alternative for celery that doesn't require a broker.

See https://www.bugsink.com/snappea-design/

![Logo](snappea-logo.png "Snappea Logo")

### Usage:

1. Add `snappea` to your `INSTALLED_APPS`.

2. Add a "snappea" DATABASE to your settings, and route snappea traffic to it:

```
DATABASES = {
    [..]
    "snappea": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'snappea.sqlite3',
        'OPTIONS': {
            'timeout': 5,
        },
    },
}
 
DATABASE_ROUTERS = ("snappea.dbrouters.SeparateSnappeaDBRouter",)

```

3. Create the tables:

```
python manage.py migrate  --database=snappea
```

4. Start the snappea background process:

```
python manage.py runsnappea
```

5. In another Window, fire off a task to test that it works:

```
python manage.py shell
Python [..] (main, [..]
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

>>> from snappea.example_tasks import printing_task
>>> printing_task.delay()
```

You should now see text in your snappea console.

### Limitations

* Django-only
* Linux-only.

