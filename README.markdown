NewLogLines
===========

newloglines.py is a small utility that prints out lines that have been added to a log file since the last time it was run. It's meant to be run from a crontab, for example if you want to check for new log entries once per hour:

    MAILTO=rolloutteam@cgnu.edu
    0 * * * * /usr/local/bin/newloglines.py /var/db/newloglines/log.db /var/log/assetsync.log

It saves the last log line in a small database, which can be shared for all logs that a user is watching. I'm using it for a few non-critical tasks like notifying our rollout team when the asset database has been updated. It makes no effort to handle unexpected events gracefully so NewLogLines is a complement to, not a replacement for, a proper [centralized logging solution](https://www.google.com/search?q=site%3Astackoverflow.com+centralized+logging).


Requirements
------------

Python 2.6+ with the built-in sqlite3 module, tested on OS X 10.6-10.8 and RHEL 6.


License
-------

Copyright 2013 Per Olofsson

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
