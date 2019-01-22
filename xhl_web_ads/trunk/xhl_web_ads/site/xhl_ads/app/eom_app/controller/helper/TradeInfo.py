class TradeInfoListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        trade_id = filter["trade_id"]
        stock_id = filter["stock_id"]
        order_a_id = filter["order_a_id"]
        order_a_user_id = filter["order_a_user_id"]
        order_a_fee_rate = filter["order_a_fee_rate"]
        order_a_fee = filter["order_a_fee"]
        order_b_id = filter["order_b_id"]
        order_b_user_id = filter["order_b_user_id"]
        order_b_fee_rate = filter["order_b_fee_rate"]
        order_b_fee = filter["order_b_fee"]
        price = filter["price"]
        count = filter["count"]
        trade_type = filter["trade_type"]
        create_time = filter["create_time"]
        log_time = filter["log_time"]
        stock_name = filter["stock_name"]
        sql="select trade_id,stock_id,order_a_id,order_a_user_id,order_a_fee_rate,order_a_fee,order_b_id,order_b_user_id,order_b_fee_rate,order_b_fee,price,count,trade_type,create_time,log_time,stock_name from trade_info where 1=1"
        if trade_id:
          sql=sql+"  and trade_id like '%"+trade_id.strip()+"%'"
        if stock_id:
          sql=sql+"  and stock_id like '%"+stock_id.strip()+"%'"
        if order_a_id:
          sql=sql+"  and order_a_id like '%"+order_a_id.strip()+"%'"
        if order_a_user_id:
          sql=sql+"  and order_a_user_id like '%"+order_a_user_id.strip()+"%'"
        if order_a_fee_rate:
          sql=sql+"  and order_a_fee_rate like '%"+order_a_fee_rate.strip()+"%'"
        if order_a_fee:
          sql=sql+"  and order_a_fee like '%"+order_a_fee.strip()+"%'"
        if order_b_id:
          sql=sql+"  and order_b_id like '%"+order_b_id.strip()+"%'"
        if order_b_user_id:
          sql=sql+"  and order_b_user_id like '%"+order_b_user_id.strip()+"%'"
        if order_b_fee_rate:
          sql=sql+"  and order_b_fee_rate like '%"+order_b_fee_rate.strip()+"%'"
        if order_b_fee:
          sql=sql+"  and order_b_fee like '%"+order_b_fee.strip()+"%'"
        if price:
          sql=sql+"  and price like '%"+price.strip()+"%'"
        if count:
          sql=sql+"  and count like '%"+count.strip()+"%'"
        if trade_type:
          sql=sql+"  and trade_type like '%"+trade_type.strip()+"%'"
        if create_time:
          sql=sql+"  and create_time like '%"+create_time.strip()+"%'"
        if log_time:
          sql=sql+"  and log_time like '%"+log_time.strip()+"%'"
        if stock_name:
          sql=sql+"  and stock_name like '%"+stock_name.strip()+"%'"
        offset = " ORDER BY ads_id DESC LIMIT {},{}".format(limit['page_index'] * limit['per_page'], limit['per_page'])
        datas = self.db_ads.execute(sql + offset).fetchall()
        lst = list()
        head=['trade_id', 'stock_id', 'order_a_id', 'order_a_user_id', 'order_a_fee_rate', 'order_a_fee', 'order_b_id', 'order_b_user_id', 'order_b_fee_rate', 'order_b_fee', 'price', 'count', 'trade_type', 'create_time', 'log_time', 'stock_name']
        for data in datas:
            temp = dict(zip(head, data))
            lst.append(temp)
        count = self.db_ads.execute("select count(*) from({}) as count_data".format(sql)).scalar()
        ret = self.set_page_params(count, limit, lst)
        self.write_json(0, data=ret)
        self.db_ads.close()


class TradeInfoAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            trade_id = args["trade_id"]
            stock_id = args["stock_id"]
            order_a_id = args["order_a_id"]
            order_a_user_id = args["order_a_user_id"]
            order_a_fee_rate = args["order_a_fee_rate"]
            order_a_fee = args["order_a_fee"]
            order_b_id = args["order_b_id"]
            order_b_user_id = args["order_b_user_id"]
            order_b_fee_rate = args["order_b_fee_rate"]
            order_b_fee = args["order_b_fee"]
            price = args["price"]
            count = args["count"]
            trade_type = args["trade_type"]
            create_time = args["create_time"]
            log_time = args["log_time"]
            stock_name = args["stock_name"]
        tradeinfo = TradeInfo()
        tradeinfo.trade_id = trade_id
        tradeinfo.stock_id = stock_id
        tradeinfo.order_a_id = order_a_id
        tradeinfo.order_a_user_id = order_a_user_id
        tradeinfo.order_a_fee_rate = order_a_fee_rate
        tradeinfo.order_a_fee = order_a_fee
        tradeinfo.order_b_id = order_b_id
        tradeinfo.order_b_user_id = order_b_user_id
        tradeinfo.order_b_fee_rate = order_b_fee_rate
        tradeinfo.order_b_fee = order_b_fee
        tradeinfo.price = price
        tradeinfo.count = count
        tradeinfo.trade_type = trade_type
        tradeinfo.create_time = create_time
        tradeinfo.log_time = log_time
        tradeinfo.stock_name = stock_name
        self.db_ads.add(tradeinfo)
        try:
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()


class TradeInfoDelHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        ids=None
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        if ids:
             self.db_ads.query(TradeInfo).filter(TradeInfo.id.in_(ids)).delete(synchronize_session=False)
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


class TradeInfoEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        ids=None
        if args is not None:
            args = json.loads(args)
            id = args["id"]
            trade_id = args["trade_id"]
            stock_id = args["stock_id"]
            order_a_id = args["order_a_id"]
            order_a_user_id = args["order_a_user_id"]
            order_a_fee_rate = args["order_a_fee_rate"]
            order_a_fee = args["order_a_fee"]
            order_b_id = args["order_b_id"]
            order_b_user_id = args["order_b_user_id"]
            order_b_fee_rate = args["order_b_fee_rate"]
            order_b_fee = args["order_b_fee"]
            price = args["price"]
            count = args["count"]
            trade_type = args["trade_type"]
            create_time = args["create_time"]
            log_time = args["log_time"]
            stock_name = args["stock_name"]
        self.db_ads.query(TradeInfo).filter(TradeInfo.id == id).update({
            TradeInfo.trade_id: trade_id,
            TradeInfo.stock_id: stock_id,
            TradeInfo.order_a_id: order_a_id,
            TradeInfo.order_a_user_id: order_a_user_id,
            TradeInfo.order_a_fee_rate: order_a_fee_rate,
            TradeInfo.order_a_fee: order_a_fee,
            TradeInfo.order_b_id: order_b_id,
            TradeInfo.order_b_user_id: order_b_user_id,
            TradeInfo.order_b_fee_rate: order_b_fee_rate,
            TradeInfo.order_b_fee: order_b_fee,
            TradeInfo.price: price,
            TradeInfo.count: count,
            TradeInfo.trade_type: trade_type,
            TradeInfo.create_time: create_time,
            TradeInfo.log_time: log_time,
            TradeInfo.stock_name: stock_name,
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


{title: 'trade_id', key: 'trade_id',width: 30},
{title: 'stock_id', key: 'stock_id',width: 30},
{title: 'order_a_id', key: 'order_a_id',width: 30},
{title: 'order_a_user_id', key: 'order_a_user_id',width: 30},
{title: 'order_a_fee_rate', key: 'order_a_fee_rate',width: 30},
{title: 'order_a_fee', key: 'order_a_fee',width: 30},
{title: 'order_b_id', key: 'order_b_id',width: 30},
{title: 'order_b_user_id', key: 'order_b_user_id',width: 30},
{title: 'order_b_fee_rate', key: 'order_b_fee_rate',width: 30},
{title: 'order_b_fee', key: 'order_b_fee',width: 30},
{title: 'price', key: 'price',width: 30},
{title: 'count', key: 'count',width: 30},
{title: 'trade_type', key: 'trade_type',width: 30},
{title: 'create_time', key: 'create_time',width: 30},
{title: 'log_time', key: 'log_time',width: 30},
{title: 'stock_name', key: 'stock_name',width: 30},

