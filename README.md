lightsout
=========

A simple daemon to turn on/off power management.


Usage
-----

Basic usage:

    lightsout start|stop|restart

Disable power management for 2 hours:

    lightsout inhibit 120

Disable power management indefinitely:

    lightsout inhibit

Re-enable power management:

    lightsout enable

Display some information about the daemon status:

    lightsout status


Dependencies
------------

- Python
- Python DBus bindings (for optional notification support)