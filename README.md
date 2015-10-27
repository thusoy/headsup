# headsup

A trivial alternative to Ubuntu's landscape-info with no external dependencies, that runs in 10% of the time of `/etc/update-motd.d/50-landscape-sysinfo`. Because perf matters.

Originally forked from https://github.com/jnweiger/landscape-sysinfo-mini/. Changes include removing utmp dependency and generally speeding things up.

Install
-------

On Debian or other platforms without a similar alternative:

    $ pip install headsup
