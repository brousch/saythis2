#!/usr/bin/env python
__all__ = ('platform', )

from os import environ
from os import path
from sys import platform as _sys_platform


class Platform(object):
    # refactored to class to allow module function to be replaced
    # with module variable

    def __init__(self):
        self._platform_ios = None
        self._platform_android = None

    def __eq__(self, other):
        return other == self._get_platform()

    def __ne__(self, other):
        return other != self._get_platform()

    def __str__(self):
        return self._get_platform()

    def __repr__(self):
        return 'platform name: \'{platform}\' from: \n{instance}'.format(
            platform=self._get_platform(),
            instance=super(Platform, self).__repr__()
        )

    def __hash__(self):
        return self._get_platform().__hash__()

    def _get_platform(self):

        if self._platform_android is None:
            # ANDROID_ARGUMENT and ANDROID_PRIVATE are 2 environment variables
            # from python-for-android project
            self._platform_android = 'ANDROID_ARGUMENT' in environ

        if self._platform_ios is None:
            self._platform_ios = (environ.get('KIVY_BUILD', '') == 'ios')

        # On android, _sys_platform return 'linux2', so prefer to check the
        # import of Android module than trying to rely on _sys_platform.
        if self._platform_android is True:
            return 'android'
        elif self._platform_ios is True:
            return 'ios'
        elif _sys_platform in ('win32', 'cygwin'):
            return 'win'
        elif _sys_platform == 'darwin':
            return 'macosx'
        elif _sys_platform[:5] == 'linux':
            return 'linux'
        return 'unknown'


platform = Platform()


def whereis_exe(program):
    ''' Tries to find the program on the system path.
        Returns the path if it is found or None if it's not found.
    '''
    path_split = ';' if platform == 'win' else ':'
    for p in environ.get('PATH', '').split(path_split):
        if path.exists(path.join(p, program)) and \
            not path.isdir(path.join(p, program)):
            return path.join(p, program)
    return None
