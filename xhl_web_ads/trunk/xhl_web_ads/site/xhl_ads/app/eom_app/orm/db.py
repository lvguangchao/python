from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

# 生成orm基类
Base = declarative_base()


class DbPools(object):

    def __init__(self):
        self._sessionfactory = None
        self._sessionfactory_ads = None
        self._sessionfactory_wealth = None
        self._sessionfactory_wealth2 = None
        self._sessionfactory_ads_entourage = None  # 从库
        self._sessionfactory_guild = None
        self._sessionfactory_detect = None
        self._sessionfactory_ads_adm = None
        self._sessionfactory_ads_plat = None

    def init(self, cfg):
        url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user, cfg.mysql_pass, cfg.mysql_ip,
                                                                      cfg.mysql_port,
                                                                      cfg.dbname)
        self.engine = create_engine(url,
                                    encoding='utf-8', echo=False,
                                    pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql

        url_ads = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user, cfg.mysql_pass, cfg.mysql_ip,
                                                                          cfg.mysql_port,
                                                                          cfg.ads_dbname)
        self.engine_ads = create_engine(url_ads,
                                        encoding='utf-8', echo=False,
                                        pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql

        url_wealth = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user, cfg.mysql_pass,
                                                                             cfg.mysql_ip, cfg.mysql_port,
                                                                             cfg.ads_dbname_wealth)
        self.engine_wealth = create_engine(url_wealth,
                                           encoding='utf-8', echo=False,
                                           pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql
        # url_wealth2 = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user2, cfg.mysql_pass2,
        #                                                                       cfg.mysql_ip2, cfg.mysql_port2,
        #                                                                       cfg.ads_dbname_wealth2)
        # self.engine_wealth2 = create_engine(url_wealth2,
        #                                     encoding='utf-8', echo=False,
        #                                     pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql

        url_guild = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user, cfg.mysql_pass,
                                                                            cfg.mysql_ip_guild, cfg.mysql_port,
                                                                            cfg.ads_dbname_guild)
        self.engine_guild = create_engine(url_guild,
                                          encoding='utf-8', echo=False,
                                          pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql

        # url_guild = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user, cfg.mysql_pass,
        #                                                                              cfg.mysql_ip, cfg.mysql_port,
        #                                                                              cfg.ads_dbname_guild)
        # self.engine_guild = create_engine(url_guild,
        #                                         encoding='utf-8', echo=False,
        #                                         pool_size=100, pool_recycle=3600)  # echo 属性=True 打印出sql

        url_ad_detect = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user_detect,
                                                                                cfg.mysql_pass_detect,
                                                                                cfg.mysql_ip_detect,
                                                                                cfg.mysql_port_detect,
                                                                                cfg.dbname_detect)
        self.engine_detect = create_engine(url_ad_detect,
                                           encoding='utf-8', echo=False,
                                           pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql

        url_ad_entourage = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user_entourage,
                                                                                   cfg.mysql_pass_entourage,
                                                                                   cfg.mysql_ip_entourage,
                                                                                   cfg.mysql_port_entourage,
                                                                                   cfg.ads_dbname_entourage)
        self.engine_entourage = create_engine(url_ad_entourage,
                                              encoding='utf-8', echo=False,
                                              pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql

        url_ad_adm = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user_adm, cfg.mysql_pass_adm,
                                                                             cfg.mysql_ip_adm, cfg.mysql_port_adm,
                                                                             cfg.ads_dbname_adm)
        self.engine_adm = create_engine(url_ad_adm,
                                        encoding='utf-8', echo=False,
                                        pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql
        url_ad_plat = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(cfg.mysql_user_plat, cfg.mysql_pass_plat,
                                                                              cfg.mysql_ip_plat, cfg.mysql_port_plat,
                                                                              cfg.ads_dbname_plat)
        self.engine_plat = create_engine(url_ad_plat,
                                         encoding='utf-8', echo=False,
                                         pool_size=80, pool_recycle=3600)  # echo 属性=True 打印出sql

    # 创建DBSession类型:
    def create_DBSession(self):
        if not self._sessionfactory:
            self._sessionfactory = sessionmaker(bind=self.engine)
        return scoped_session(self._sessionfactory)

    def create_Ads_DBSession(self):
        if not self._sessionfactory_ads:
            self._sessionfactory_ads = sessionmaker(bind=self.engine_ads)
        return scoped_session(self._sessionfactory_ads)  # scoped_session session生命周期管理

    def create_Wealth_DBSession(self):
        if not self._sessionfactory_wealth:
            self._sessionfactory_wealth = sessionmaker(bind=self.engine_wealth)
        return scoped_session(self._sessionfactory_wealth)  # scoped_session session生命周期管理

    def create_Wealth_DBSession2(self):
        if not self._sessionfactory_wealth2:
            self._sessionfactory_wealth2 = sessionmaker(bind=self.engine_wealth2)
        return scoped_session(self._sessionfactory_wealth2)

    def create_guild_DBSession(self):
        if not self._sessionfactory_guild:
            self._sessionfactory_guild = sessionmaker(bind=self.engine_guild)
        return scoped_session(self._sessionfactory_guild)  # scoped_session session生命周期管理

    def create_detect_DBSession(self):
        if not self._sessionfactory_detect:
            self._sessionfactory_detect = sessionmaker(bind=self.engine_detect)
        return scoped_session(self._sessionfactory_detect)

    def create_entourage_DBSession(self):
        if not self._sessionfactory_ads_entourage:
            self._sessionfactory_ads_entourage = sessionmaker(bind=self.engine_entourage)
        return scoped_session(self._sessionfactory_ads_entourage)

    def create_adm_DBSession(self):
        if not self._sessionfactory_ads_adm:
            self._sessionfactory_ads_adm = sessionmaker(bind=self.engine_adm)
        return scoped_session(self._sessionfactory_ads_adm)

    def create_plat_DBSession(self):
        if not self._sessionfactory_ads_plat:
            self._sessionfactory_ads_plat = sessionmaker(bind=self.engine_plat)
        return scoped_session(self._sessionfactory_ads_plat)


_db = DbPools()
del DbPools


def app_db():
    global _db
    return _db
