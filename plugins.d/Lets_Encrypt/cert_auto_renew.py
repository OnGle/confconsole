"""Enable/Disable cert auto-renew"""

from os import chmod, stat, path, getenv
import sys

CRON_PATH='/etc/cron.daily/confconsole-dehydrated'

def enable_cron():
    st = stat(CRON_PATH)
    chmod(CRON_PATH, st.st_mode | 0o111)

def disable_cron():
    st = stat(CRON_PATH)
    chmod(CRON_PATH, st.st_mode ^ 0o111)

def check_cron():
    if path.isfile(CRON_PATH):
        st = stat(CRON_PATH)
        return st.st_mode & 0o111 == 0o111
    else:
        return 'fail'

def run():
    ev_enabled = 'enabled' if getenv('CC_LETSENCRYPT_AUTORENEW') == 'y' else 'disabled'

    enabled = check_cron()
    if enabled == 'fail':
        msg = '''Cron job for dehydrated does not exist.\nPlease "Get certificate" first.'''
        if interactive:
            r = console.msgbox('Error', msg)
        sys.stderr.write('Error: %s\n' % msg)
    else:
        status = 'enabled' if enabled else 'disabled'
        msg = '''Automatic certificate renewal is currently {}''' 

        if interactive:
            r = console._wrapper('yesno', msg.format(status), 10, 30, yes_label='Toggle', no_label='Ok')
            while r == 0:
                if enabled:
                    disable_cron()
                else:
                    enable_cron()
                enabled = check_cron()
                status = 'enabled' if enabled else 'disabled'
                r = console._wrapper('yesno', msg.format(status), 10, 30, yes_label='Toggle', no_label='Ok') 
        else:
            if status != ev_enabled:
                if ev_enabled == 'enabled':
                    enable_cron()
                else:
                    disable_cron()
