# -*- coding: utf-8 -*-
import os, time, sys, signal, multiprocessing
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.web
from eom_app.controller import controllers
from eom_common.eomcore.logger import log
from .configs import app_cfg
from .session import swx_session
from eom_app.orm.db import app_db
from eom_app.controller.helper.uploadManager import app_upManager
# from eom_app.controller.helper.auto_task import AutoTask

app_upManager = app_upManager()
from eom_app.controller.helper.identity import app_map

cfg = app_cfg()  # 配置文件对象
db = app_db()  # 数据库对象


def handler(signum, frame):
    global is_exit
    is_exit = True
    log.v("receive a signal %d, is_exit = %d\n" % (signum, is_exit))
    try:
        tornado.ioloop.IOLoop.instance().stop()
        log.v("tornado stop\n")
    except:
        print("tornado error")

    try:
        # get_obs_manager().to_stoped()
        log.v("thread stop\n")
    except:
        print("thread stop error")

    try:
        # get_obs_manager().save_file()
        log.v("process exit\n")
    except:
        print("process exit error")
    try:
        sys.exit(0)
        log.v("sys exit\n")
    except:
        print("sys exit error")

    sys.exit(0)


class SwxCore:
    def __init__(self):
        # self._cfg = ConfigFile()
        pass

    def init(self, options):
        if 'app_path' not in options:
            return False
        else:
            cfg.app_path = options['app_path']

        if not self._load_config(options):
            return False

        if 'static_path' in options:
            cfg.static_path = options['static_path']
        else:
            cfg.static_path = os.path.join(options['app_path'], 'static')

        if 'data_path' in options:
            cfg.data_path = options['data_path']
        else:
            cfg.data_path = os.path.join(options['app_path'], 'data')

        if 'template_path' in options:
            cfg.template_path = options['template_path']
        else:
            cfg.template_path = os.path.join(options['app_path'], 'view')

        if 'res_path' in options:
            cfg.res_path = options['res_path']
        else:
            cfg.res_path = os.path.join(options['app_path'], 'res')

        if not swx_session().init():
            return False

        if sys.platform == 'win32':
            signal.signal(signal.SIGINT, handler)
            signal.signal(signal.SIGTERM, handler)
        else:
            signal.signal(signal.SIGUSR1, handler)
            signal.signal(signal.SIGINT, handler)
            signal.signal(signal.SIGTERM, handler)
        return True

    def _load_config(self, options):
        if 'cfg_path' in options:
            _cfg_path = options['cfg_path']
        else:
            _cfg_path = os.path.join(options['app_path'], 'conf')

        _cfg_file = os.path.join(_cfg_path, 'web-xhl-rank.conf')
        # _cfg_file = os.path.join(_cfg_path, 'web-xhl-rank-release.conf')
        if os.path.exists(_cfg_file):
            if not cfg.load(_cfg_file):
                return False
            else:
                cfg.dev_mode = True
        else:
            cfg.dev_mode = False

        cfg.cfg_path = _cfg_path

        return True

    @staticmethod
    def _daemon():
        # fork for daemon.
        if sys.platform == 'win32':
            log.v('os.fork() not support Windows, operation ignored.\n')
            return True

        try:
            pid = os.fork()
            if pid > 0:
                log.w('parent #1 exit.{}====={}====={}\n'.format(pid, os.getpid(), os.getppid()))
                # return False
                os._exit(0)
        except OSError:
            log.e('fork #1 failed.\n')
            os._exit(1)

        # Detach from parent env.
        os.chdir('/')
        os.umask(0)
        os.setsid()

        # Second fork.
        try:
            pid = os.fork()
            if pid > 0:
                log.w('parent #2 exit.{}====={}====={}\n'.format(pid, os.getpid(), os.getppid()))
                os._exit(0)
        except OSError:
            log.e('fork #2 failed.\n')
            # return False
            os._exit(1)

        # OK I'm daemon now.
        for f in sys.stdout, sys.stderr:
            f.flush()
        si = open('/dev/null', 'r')
        so = open('/dev/null', 'a+')
        se = open('/dev/null', 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        return True

    def run(self):
        settings = {
            #
            'cookie_secret': '8946svdABGD345fg98uhIaefEBePIfegOIakjFH43oETzK',

            'login_url': '/login',

            # 指定静态文件的路径，页面模板中可以用 {{ static_url('css/main.css') }} 的方式调用
            'static_path': cfg.static_path,

            # 指定模板文件的路径
            'template_path': cfg.template_path,

            # 防止跨站伪造请求，参见 http://old.sebug.net/paper/books/tornado/#_7
            'xsrf_cookies': False,

            'autoescape': 'xhtml_escape',

            # 'ui_modules': ui_modules,
            'debug': True

            # Debug Mode.
            # 'compiled_template_cache': False,
            # 'static_hash_cache': False,
        }
        # if cfg.debug:
        #     settings['compiled_template_cache'] = False
        #     settings['static_hash_cache'] = False
        web_app = tornado.web.Application(controllers, **settings)
        log.w('a tornado io-loop exit.\n')
        log.w('系统正在初始化，请耐心等待...\n')
        db.init(cfg)  # 数据库初始化
        app_upManager.task_destroy()
        # 全自动化审核
        # at = AutoTask()
        # at.start()

        log.w('系统正在初始化开始...\n')
        app_map().Baseuser()
        app_map().TLogWithdrawAnchor()
        app_map().getRoomInfo()
        log.w('系统初始化房间信息完成。\n')
        app_map().unionid2nameMap()
        app_map().getPlayLogMap()
        log.w('系统初始化播放记录信息完成。\n')
        app_map().Baseuser()
        app_map().Baseuserroom()
        app_map().Adsuniongroup()
        app_map().Baseunion()
        log.w('系统初始化Baseunion完成。\n')
        app_map().AgentInfo()
        app_map().get_platform_map_list()
        app_map().init_user_info_map()
        log.w('系统初始化完成。\n')

        if sys.platform == 'win32':
            web_app.listen(cfg.server_port)
            log.v('Web Server start on http://127.0.0.1:{} {}\n'.format(cfg.server_port, cfg.debug))
            tornado.ioloop.IOLoop.instance().start()
            print('eeeee')
        else:
            if not cfg.debug:
                log.set_attribute(console=False, filename='/var/log/rank/rank.log')
                if not self._daemon():
                    return False
                # 进入daemon模式了，不再允许输出信息到控制台了
                log.v('\n====================================={}======{}\n'.format(os.getpid(), os.getppid()))

                def _run(port):
                    log.w('obs stat wait ========.\n')
                    log.w('obs stat wait end ========.\n')
                    loop = True
                    count = 0
                    while loop:
                        try:
                            log.v('Web Server start on http://127.0.0.1:{}==={}\n'.format(port, os.getpid()))
                            web_app.listen(port)
                            loop = False
                        except Exception as e:
                            loop = True
                            count += 1
                            log.v('count = {} web_app.listen failed = {}\n'.format(count, e))
                            time.sleep(5)
                    tornado.ioloop.IOLoop.instance().start()
                    log.w('a tornado io-loop exit.\n')

                jobs = list()
                port = cfg.server_port
                for x in range(cfg.server_worker):
                    p = multiprocessing.Process(target=_run, args=(port,))
                    jobs.append(p)
                    p.start()
                    port += 1
            else:
                web_app.listen(cfg.server_port)
                log.set_attribute(console=True, filename='/var/log/rank/rank.log')
                log.v('Web Server start on http://127.0.0.1:{}\n'.format(cfg.server_port))
                tornado.ioloop.IOLoop.instance().start()

        # server = tornado.httpserver.HTTPServer(web_app)
        # server.listen(cfg.server_port)
        # log.v('Web Server start on http://127.0.0.1:{}\n'.format(cfg.server_port))
        # tornado.ioloop.IOLoop.instance().start()
        return 0
