# -*- coding: utf-8 -*-

# 检测运行环境和相对定位文件路径

import os
import platform
import sys

__all__ = ['PATH_APP_ROOT', 'PATH_LOG', 'PATH_CONF', 'PATH_DATA']

PATH_LOG = ''
PATH_CONF = ''
PATH_DATA = ''

# 将Python安装的扩展库移除，避免开发调试与正式发布所依赖的库文件不一致导致发布出去的版本无法运行
x = []
for p in sys.path:
    if p.find('site-packages') != -1 or p.find('dist-packages') != -1:
        x.append(p)
for p in x:
    sys.path.remove(p)

PLATFORM = platform.system().lower()
if PLATFORM not in ['windows', 'linux']:
    sys.exit(1)

BITS = 'x64'
if '32bit' == platform.architecture()[0]:
    BITS = 'x86'

path_of_this_file = os.path.abspath(os.path.dirname(__file__))
print('this path: ', path_of_this_file)

# 根据是否打包，以及相对路径是否存在等信息判断当前是在开发调试还是发布的版本
IN_ZIP = False
DEV_MODE = True

# 如果已经打包了，这一定是发布版本
# os.path.abspath(os.path.join(path_of_this_file, '..', '..'))
PATH_APP_ROOT = path_of_this_file
if PATH_APP_ROOT[-4:].lower() == '.zip':
    print('---in-zip---')
    PATH_APP_ROOT = os.path.abspath(os.path.join(PATH_APP_ROOT, '..'))
    IN_ZIP = True
    DEV_MODE = False
else:
    PATH_APP_ROOT = os.path.abspath(os.path.join(PATH_APP_ROOT, '..'))
    # 如果没有打包，可能是开发版本，也可能是发布源代码版本，需要进一步判断
    if os.path.exists(
        os.path.join(
            path_of_this_file,
            '..',
            '..',
            '..',
            'packages',
            'common',
            'eom_common')):
        DEV_MODE = True
    else:
        DEV_MODE = False

if DEV_MODE:
    # 开发调试模式
    _ext_path = os.path.abspath(
        os.path.join(
            path_of_this_file,
            '..',
            '..',
            '..',
            'packages',
            'common'))
    if _ext_path not in sys.path and os.path.exists(_ext_path):
        sys.path.append(_ext_path)

    _ext_path = os.path.abspath(
        os.path.join(
            path_of_this_file,
            '..',
            '..',
            '..',
            'packages',
            'packages-common'))
    if _ext_path not in sys.path:
        sys.path.append(_ext_path)

    _ext_path = os.path.abspath(
        os.path.join(
            path_of_this_file,
            '..',
            '..',
            '..',
            'packages',
            'packages-{}'.format(PLATFORM),
            BITS))
    if _ext_path not in sys.path:
        sys.path.append(_ext_path)

    PATH_LOG = os.path.abspath(os.path.join(path_of_this_file, '..', 'log'))
    PATH_CONF = os.path.abspath(os.path.join(path_of_this_file, '..', 'conf'))
    # PATH_DATA = os.path.abspath(os.path.join(path_of_this_file, '..', '..', '..', '..', 'share', 'data'))

else:
    # 未打包的发布路径（发布源代码）
    #   web_root
    #     |- app
    #     |   |- eom_common
    #     |   \- eom_app
    #     |- static
    #     |- view
    #     \- packages
    #          |- packages-common
    #          \- packages-windows   or   packages-linux
    # --------------------------------------------------------------
    # 打包后的发布路径
    #   web_root
    #     |- app.zip
    #     |- static
    #     |- view
    #     \- packages
    #          |- packages-common
    #          \- packages-windows   or   packages-linux

    _ext_path = os.path.abspath(
        os.path.join(
            PATH_APP_ROOT,
            'packages',
            'packages-common'))
    if _ext_path not in sys.path:
        sys.path.append(_ext_path)
        print('add path: ', _ext_path)

    _ext_path = os.path.abspath(
        os.path.join(
            PATH_APP_ROOT,
            'packages',
            'packages-{}'.format(PLATFORM),
            BITS))
    if _ext_path not in sys.path:
        sys.path.append(_ext_path)
        print('add path: ', _ext_path)

    PATH_LOG = os.path.abspath(os.path.join(path_of_this_file, '..', 'log'))
    PATH_CONF = os.path.abspath(os.path.join(path_of_this_file, '..', 'conf'))

if PLATFORM == 'linux':
    PATH_LOG = '/var/log/eom/web-gather'

print('sys-path:', sys.path)
print('path-log:', PATH_LOG)
print('path-conf:', PATH_CONF)
