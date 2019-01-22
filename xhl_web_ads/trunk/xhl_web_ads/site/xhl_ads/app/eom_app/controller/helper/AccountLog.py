class AccountLogListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        act_log_id = filter["act_log_id"]
        xhl_union_id = filter["xhl_union_id"]
        trade_num = filter["trade_num"]
        income = filter["income"]
        income_type = filter["income_type"]
        comment = filter["comment"]
        create_time = filter["create_time"]
        log_time = filter["log_time"]
        sql="select act_log_id,xhl_union_id,trade_num,income,income_type,comment,create_time,log_time from account_log where 1=1"
        if act_log_id:
          sql=sql+"  and act_log_id like '%"+act_log_id.strip()+"%'"
        if xhl_union_id:
          sql=sql+"  and xhl_union_id like '%"+xhl_union_id.strip()+"%'"
        if trade_num:
          sql=sql+"  and trade_num like '%"+trade_num.strip()+"%'"
        if income:
          sql=sql+"  and income like '%"+income.strip()+"%'"
        if income_type:
          sql=sql+"  and income_type like '%"+income_type.strip()+"%'"
        if comment:
          sql=sql+"  and comment like '%"+comment.strip()+"%'"
        if create_time:
          sql=sql+"  and create_time like '%"+create_time.strip()+"%'"
        if log_time:
          sql=sql+"  and log_time like '%"+log_time.strip()+"%'"
        offset = " ORDER BY ads_id DESC LIMIT {},{}".format(limit['page_index'] * limit['per_page'], limit['per_page'])
        datas = self.db_ads.execute(sql + offset).fetchall()
        lst = list()
        head=['act_log_id', 'xhl_union_id', 'trade_num', 'income', 'income_type', 'comment', 'create_time', 'log_time']
        for data in datas:
            temp = dict(zip(head, data))
            lst.append(temp)
        count = self.db_ads.execute("select count(*) from({}) as count_data".format(sql)).scalar()
        ret = self.set_page_params(count, limit, lst)
        self.write_json(0, data=ret)
        self.db_ads.close()


class AccountLogAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            act_log_id = args["act_log_id"]
            xhl_union_id = args["xhl_union_id"]
            trade_num = args["trade_num"]
            income = args["income"]
            income_type = args["income_type"]
            comment = args["comment"]
            create_time = args["create_time"]
            log_time = args["log_time"]
        accountlog = AccountLog()
        accountlog.act_log_id = act_log_id
        accountlog.xhl_union_id = xhl_union_id
        accountlog.trade_num = trade_num
        accountlog.income = income
        accountlog.income_type = income_type
        accountlog.comment = comment
        accountlog.create_time = create_time
        accountlog.log_time = log_time
        self.db_ads.add(accountlog)
        try:
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()


class AccountLogDelHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        ids=None
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        if ids:
             self.db_ads.query(AccountLog).filter(AccountLog.id.in_(ids)).delete(synchronize_session=False)
        else:
            self.write(-1,'没有id')
            return
        try:
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


class AccountLogEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        ids=None
        if args is not None:
            args = json.loads(args)
            id = args["id"]
            act_log_id = args["act_log_id"]
            xhl_union_id = args["xhl_union_id"]
            trade_num = args["trade_num"]
            income = args["income"]
            income_type = args["income_type"]
            comment = args["comment"]
            create_time = args["create_time"]
            log_time = args["log_time"]
        self.db_ads.query(AccountLog).filter(AccountLog.id == id).update({
            AccountLog.act_log_id: act_log_id,
            AccountLog.xhl_union_id: xhl_union_id,
            AccountLog.trade_num: trade_num,
            AccountLog.income: income,
            AccountLog.income_type: income_type,
            AccountLog.comment: comment,
            AccountLog.create_time: create_time,
            AccountLog.log_time: log_time,
        })
        try:
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "修改失败")
        finally:
            self.db_ads.close()


{title: 'act_log_id', key: 'act_log_id',width: 30},
{title: 'xhl_union_id', key: 'xhl_union_id',width: 30},
{title: 'trade_num', key: 'trade_num',width: 30},
{title: 'income', key: 'income',width: 30},
{title: 'income_type', key: 'income_type',width: 30},
{title: 'comment', key: 'comment',width: 30},
{title: 'create_time', key: 'create_time',width: 30},
{title: 'log_time', key: 'log_time',width: 30},


class AccountLog(Base):
    __tablename__ = "account_log"
    act_log_id = Column(Integer)
    xhl_union_id = Column(VARCHAR(255))
    trade_num = Column(VARCHAR(255))
    income = Column()
    income_type = Column(Integer)
    comment = Column(VARCHAR(255))
    create_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)



