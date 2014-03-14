import sys
import time
import subprocess

try:
    import dbus
except ImportError:
    dbus = None

from daemon import Daemon

USAGE = '''Usage: lightsout start|stop|restart|enable|status|inhibit'''


def send_notification(message, error=False):
    bus = dbus.SessionBus()
    notifications = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    notify = dbus.Interface(notifications, 'org.freedesktop.Notifications')

    if error:
        notify.Notify('Power Management', 0, 'dialog-error', 'Power Management', message, '', '', 6000)
    else:
        notify.Notify('Power Management', 0, 'screensaver', 'Power Management', message, '', '', 6000)


class DPMSManager(Daemon):
    def run(self):
        while True:
            time.sleep(1)

    def enable(self):
        subprocess.call(['xset', 'dpms'])
        subprocess.call(['xset', 's', 'on'])

        if dbus:
            send_notification('Re-enabled')

    def inhibit(self, minutes=None):
        subprocess.call(['xset', '-dpms'])
        subprocess.call(['xset', 's', 'off'])

        if dbus:
            if minutes:
                send_notification('Disabled for %s minutes' % time)
                self.timer(minutes)
            else:
                send_notification('Disabled')

    def timer(self, minutes):
        time.sleep(minutes * 60)
        self.enable()

    def status(self):
        dpm_status = subprocess.Popen('xset -q | grep -ce \'DPMS is Enabled\'', shell=True,
                                      stdout=subprocess.PIPE).communicate()[0]
        screensaver_status = subprocess.Popen('xset -q | grep -ce \'timeout:  600\'', shell=True,
                                              stdout=subprocess.PIPE).communicate()[0]

        print('Power management enabled : %s' % bool(int(dpm_status)))
        print('Screensaver enabled      : %s' % bool(int(screensaver_status)))


if __name__ == '__main__':
    daemon = DPMSManager('/tmp/dpms_manager.pid')

    if len(sys.argv) >= 2:
        arg = sys.argv[1]

        if arg == 'start':
            daemon.start()

        elif arg == 'stop':
            daemon.stop()

        elif arg == 'restart':
            daemon.restart()

        elif arg == 'inhibit':
            if len(sys.argv) == 3:
                t = int(sys.argv[2])

            else:
                t = None
            daemon.inhibit(t)

        elif arg == 'enable':
            daemon.enable()

        elif arg == 'status':
            daemon.status()

        else:
            print(USAGE)
            sys.exit(2)

        sys.exit(0)

    else:
        print(USAGE)
        sys.exit(2)