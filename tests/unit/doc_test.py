# -*- coding: utf-8 -*-
'''
    tests.unit.doc_test
    ~~~~~~~~~~~~~~~~~~~~
'''

# Import Python libs
from __future__ import absolute_import
import os

# Import Salt Testing libs
from salttesting import TestCase
from salttesting.helpers import ensure_in_syspath

# Import Salt libs
import salt.modules.cmdmod

ensure_in_syspath('../')


class DocTestCase(TestCase):
    '''
    Unit test case for testing doc files and strings.
    '''

    def test_check_for_doc_inline_markup(self):
        '''
        We should not be using the ``:doc:`` inline markup option when
        cross-referencing locations. Use ``:ref:`` or ``:mod:`` instead.

        This test checks for reference to ``:doc:`` usage.

        See Issue #12788 for more information.

        https://github.com/saltstack/salt/issues/12788
        '''
        salt_dir = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 2)[0]
        salt_dir += '/'
        cmd = 'grep -r :doc: ' + salt_dir

        grep_call = salt.modules.cmdmod.run_stdout(cmd=cmd).split('\n')

        test_ret = {}
        for line in grep_call:
            # Skip any .pyc files that may be present
            if line.startswith('Binary'):
                continue

            key, val = line.split(':', 1)

            # Don't test man pages or this file
            if 'man' in key or key.endswith('doc_test.py'):
                continue

            # Don't test the page that documents to not use ":doc:"
            if key.endswith('/conventions/documentation.rst'):
                continue

            # Set up test return dict
            if test_ret.get(key) is None:
                test_ret[key] = [val.lstrip()]
            else:
                test_ret[key].append(val.lstrip())

        # Allow test results to show files with :doc: ref, rather than truncating
        self.maxDiff = None

        # test_ret should be empty, otherwise there are :doc: references present
        self.assertEqual(test_ret, {})


if __name__ == '__main__':
    from integration import run_tests
    run_tests(DocTestCase, needs_daemon=False)
