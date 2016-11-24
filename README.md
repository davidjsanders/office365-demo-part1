# office365-demo-part1
Accessing Office 365 from Python and Flask - Part 1
## An important note ##
The configuration file (config.json or o365-demo.json) should
NEVER be in a code repository. It contains your
application's unique identifier (a 4 word uuid) which is a
valuable secret.

Place this file
somewhere safe (e.g. ~/.mysecrets/o365-demo.json) and change the
rights (e.g. chmod 0600 ~/.mysecrets/o365-demo.json). To use the
configuration file, set your environment variable config to point
to it; for example: export config="~/.mysecrets/o365-demo.json"

Then run the app. If running the app with Docker, then pass the
env variable to Docker and map the file location, e.g.:

 docker run --env config="/home/pycred/.mysecrets/o365-demo.json" \
   --volume /home/localuser/.mysecrets/:/home/pycred/.mysecrets \
   ...

