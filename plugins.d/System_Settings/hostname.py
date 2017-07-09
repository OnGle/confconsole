'''Update machine hostname'''

import os
import re
from subprocess import Popen, CalledProcessError, PIPE

TITLE = 'Update Hostname'

def set_hostname(hostname):
    proc = Popen(["hostname", hostname], stderr=PIPE)
    _, out = proc.communicate()
    returncode = proc.returncode

    if returncode:
        return (returncode, out)
        #console.msgbox(TITLE, '{} ({})'.format(out, new_hostname))

    with open('/etc/hostname', 'w') as fob:
        fob.write(hostname + '\n')

    with open('/etc/hosts', 'r') as fob:
        lines = fob.readlines()
    with open('/etc/hosts', 'w') as fob:
        for line in lines:
            fob.write(re.sub(r'^127\.0\.1\.1 .*', '127.0.1.1 ' + hostname, line))

    with open('/etc/postfix/main.cf', 'r') as fob:
        lines = fob.readlines()
    with open('/etc/postfix/main.cf', 'w') as fob:
        for line in lines:
            fob.write(re.sub(r'myhostname =.*', 'myhostname = {}'.format(hostname), line))

    return (0, None)



def run():
    if interactive:
        while True:
            ret, hostname = console.inputbox(TITLE, 'Please enter the new hostname for this machine:')
            if ret == 0: # data inputed
                ret, out = set_hostname(hostname)
                if ret != 0: # hostname change failed
                    console.msgbox(TITLE, '{} ({})'.format(out, hostname))
                    continue
                else:
                    break
            else:
                return

        os.system('postfix reload')
        console.msgbox(TITLE, 'Hostname updated successfully. Some applications might require a relaunch before the setting applies to them.')

    else:
        hostname = os.getenv('CC_HOSTNAME_HOSTNAME')
        ret, out = set_hostname(hostname)
        if ret:
            print(out)
        else:
            os.system('postfix reload')
