
#How to access the log

0. Install necessary package:
   a) Install Google Cloud SDK here : https://cloud.google.com/sdk/docs/
   b) Download and install App Engine SDK for python: https://cloud.google.com/appengine/docs/python/download
   c) Run GoogleAppEngineLauncher.app -> Make Symlinks
   d) PYTHONPATH="$PYTHONPATH:/usr/local/google_appengine:/usr/local/google_appengine/lib:/usr/local/google_appengine/lib/yaml/"

1. Go to https://console.cloud.google.com/home/dashboard?project=poem-156922
2. Backup the entities from datastore to google storeage (bucket: poem-backup) (refer to https://cloud.google.com/appengine/docs/python/console/datastore-backing-up-restoring)
   a) Resource -> Cloud Datastore -> Admin -> Open Datastore Admin
   b) Select poem, then "Backup Entities"
   c) Use the default name; Bucket name is "poem-backup"; Click "Backup Entitiles"
3. Download the data to local folder using google_cloud/download.sh
4. Read the data using google_could/read.py


#Where to change the default weight: 
1. poem.js
2. poem_interactive.js && poem_interactive_experiment.js (only the encourage_file related weight)


Change log:

Add "self-destruction" to the curse words [1/27/2017]
