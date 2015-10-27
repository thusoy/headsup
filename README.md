# headsup

A trivial alternative to Ubuntu's landscape-info with no external dependencies, that runs in 10% of the time of `/etc/update-motd.d/50-landscape-sysinfo`. Because perf matters.

Originally forked from https://github.com/jnweiger/landscape-sysinfo-mini/. Changes include removing utmp dependency and generally speeding things up.


Install
-------

If you want the `headsup` command available:

    $ pip install headsup

If you just want to replace the Ubuntu default, copy the `headsup.py` file into `/etc/updated-motd.d/50-headsup` (and remove the standard Ubuntu one if present) and make the script executable. `pam_motd` runs these scripts in order to create the motd.


Usage
-----

    $ headsup

      System information as of Tue Oct 27 14:21:53 2015

      System load:  16.0%              Processes:        104
      Usage of /:   54.7% of 68.63GB   Users logged in:  3
      Memory usage: 28.4%              IP address for wlan0: 10.3.12.75
      Swap usage:   ---
