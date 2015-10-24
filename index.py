import json
import os
import plistlib
import re
import sublime

DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS = {
    'magicpython_python2': 'python2'
}

DEBUG = True

FLAGS = {}

SCHEDULE_PERIOD = 2000
REATTACH_TIMEOUT = 2000

_safe_expr_re = re.compile(r'^([\s\w!&|$]+|[!|&]\s*\(|\))+$')


class Compiler:
    def __init__(self, settings, debug=False):
        self._scheduled = False
        self._last_settings = FLAGS
        self._settings = settings
        self._debug = debug

    def log(self, *args):
        new_args = ('MagicPython:',) + tuple(args) #py2 compat
        if self._debug:
            print(new_args)

    def schedule_sync(self):
        if self._scheduled:
            return

        self.log('schedule sync; detach pref listeners')
        sublime.status_message('Regenerating MagicPython syntax files...')
        self.detach()
        self._scheduled = True
        sublime.set_timeout(self.sync, SCHEDULE_PERIOD)

    def read_settings(self):
        ns = {}
        for key in FLAGS:
            val = self._settings.get('magicpython_%s' % (key,))
            if val is None:
                ns[key] = FLAGS[key]
            else:
                ns[key] = val
        return ns

    def sync(self):
        self._scheduled = False

        new_settings = self.read_settings()
        if new_settings == self._last_settings:
            self.log('sync: no changes from last time; aborting')
            sublime.set_timeout(self.on_sync_done, REATTACH_TIMEOUT)
            return

        self.log('sync: regenerating')
        self._last_settings = new_settings

        ns = dict(new_settings)
        ns.update({
            '__builtins__': {},
            'builtins': {},
        })

        in_fn = os.path.join(DIR, 'grammars', 'tpl',
                             'MagicPython.tmLanguage.tpl')

        data = plistlib.readPlist(in_fn)
        out_fn = os.path.join(DIR, 'grammars',
                              'MagicPython.tmLanguage')

        data = plistlib.readPlist(in_fn)

        def eval_condition(cond):
            if not _safe_expr_re.match(cond):
                return False

            cond = cond.replace('&&', ' and ') \
                       .replace('||', ' or ') \
                       .replace('!', ' not ')

            try:
                return eval(cond, ns, ns)
            except Exception as ex:
                # TODO
                return False

        def visit(data):
            def _visit(rule):
                if 'patterns' not in rule:
                    return

                new_pats = []
                pats = rule['patterns']
                for pat in pats:
                    if 'condition' in pat:
                        if eval_condition(pat['condition']):
                            new_pats.append(pat)
                    else:
                        new_pats.append(pat)
                rule['patterns'] = new_pats

            if data.get('repository'):
                for rule in data['repository'].values():
                    _visit(rule)

        visit(data)
        plistlib.writePlist(data, out_fn)

        sublime.set_timeout(self.on_sync_done, REATTACH_TIMEOUT)

    def on_sync_done(self):
        sublime.status_message('MagicPython syntax has been regenerated.')
        new_settings = self.read_settings()
        if new_settings == self._last_settings:
            self.log('after sync: attaching pref listeners')
            self.attach()
        else:
            # While we were generating the updated syntax, the user
            # has updated the settings again. Schedule another sync.
            self.log('after sync: re-syncing')
            self.schedule_sync()

    def attach(self):
        if not hasattr(self._settings, 'add_on_change'):
            self.log('settings.add_on_change API is not available')
            return

        add_on_change = lambda name: self._settings.add_on_change(
            name, lambda: (print(name), self.schedule_sync()))

        for prop in SETTINGS:
            add_on_change(prop)

    def detach(self):
        if not hasattr(self._settings, 'clear_on_change'):
            self.log('settings.clear_on_change API is not available')
            return

        for prop in SETTINGS:
            self._settings.clear_on_change(prop)


def plugin_loaded():
    global SETTINGS, FLAGS

    settings = sublime.load_settings("Preferences.sublime-settings")

    flags_fn = outFn = os.path.join(DIR, 'grammars', 'src', 'flags.json')
    f = open(flags_fn, 'r')
    try:
        data = json.load(f)
        FLAGS = data
        SETTINGS = dict([('magicpython_%s' % (k,), k) for k in data])
    finally:
        f.close()

    compiler = Compiler(settings, debug=DEBUG)
    compiler.attach()
    compiler.schedule_sync()
