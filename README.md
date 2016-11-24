# office365-demo-part1
Accessing Office 365 from Python and Flask - Part 1
## An important note on configuration ##
The configuration file (o365-demo.json or whatever you decide
to call it) should NEVER be in the code repository, particularly
if you fork the sample which means it will remain public. It contains
sensitive secrets like your application's unique identifier (a 4 word uuid).

Place this file somewhere safe (e.g. ~/.mysecrets/o365-demo.json) and change the
rights to be read/write only by the owner (e.g. chmod 0600 ~/.mysecrets/o365-demo.json).
To use the configuration file, set the environment variable o365_demo_config to point
to it; for example: export o365_demo_config="~/.mysecrets/o365-demo.json".

If the environment variable o365_demo_config is not set, then a Python KeyError will
be raised. If the file cannot be found, then a Python FileNotFoundError will be
raised.

After the file has been set, and the environment variable defined, the app can be
run by typing: python app.py (this assumes a virtual environment as defined by
requirements.txt has been setup or the pip installs run manually for the required
packages.)

If running the app with Docker (either the predefined image dsanderscan/o365-demo-pt1
or by building your own), the env variable must be passed to Docker and the file location
of the config file mapped, e.g.:

```
 docker run --env o365_demo_config="/home/pycred/.mysecrets/o365-demo.json" \
   --volume /home/localuser/.mysecrets/:/home/pycred/.mysecrets \
   ...
```
