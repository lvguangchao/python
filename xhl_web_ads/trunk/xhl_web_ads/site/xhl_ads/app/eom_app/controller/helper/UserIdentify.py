class UserIdentifyListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        identify_id = filter["identify_id"]
        xhl_union_id = filter["xhl_union_id"]
        identify_name = filter["identify_name"]
        identify_type = filter["identify_type"]
        identify_card = filter["identify_card"]
        country = filter["country"]
        sex = filter["sex"]
        birthday = filter["birthday"]
        status = filter["status"]
        is_employee = filter["is_employee"]
        phone_num = filter["phone_num"]
        identify_img_front = filter["identify_img_front"]
        identify_img_back = filter["identify_img_back"]
        verify_status = filter["verify_status"]
        log_time = filter["log_time"]
        create_time = filter["create_time"]
        sql="select identify_id,xhl_union_id,identify_name,identify_type,identify_card,country,sex,birthday,status,is_employee,phone_num,identify_img_front,identify_img_back,verify_status,log_time,create_time from user_identify where 1=1"
        if identify_id:
          sql=sql+"  and identify_id like '%"+identify_id.strip()+"%'"
        if xhl_union_id:
          sql=sql+"  and xhl_union_id like '%"+xhl_union_id.strip()+"%'"
        if identify_name:
          sql=sql+"  and identify_name like '%"+identify_name.strip()+"%'"
        if identify_type:
          sql=sql+"  and identify_type like '%"+identify_type.strip()+"%'"
        if identify_card:
          sql=sql+"  and identify_card like '%"+identify_card.strip()+"%'"
        if country:
          sql=sql+"  and country like '%"+country.strip()+"%'"
        if sex:
          sql=sql+"  and sex like '%"+sex.strip()+"%'"
        if birthday:
          sql=sql+"  and birthday like '%"+birthday.strip()+"%'"
        if status:
          sql=sql+"  and status like '%"+status.strip()+"%'"
        if is_employee:
          sql=sql+"  and is_employee like '%"+is_employee.strip()+"%'"
        if phone_num:
          sql=sql+"  and phone_num like '%"+phone_num.strip()+"%'"
        if identify_img_front:
          sql=sql+"  and identify_img_front like '%"+identify_img_front.strip()+"%'"
        if identify_img_back:
          sql=sql+"  and identify_img_back like '%"+identify_img_back.strip()+"%'"
        if verify_status:
          sql=sql+"  and verify_status like '%"+verify_status.strip()+"%'"
        if log_time:
          sql=sql+"  and log_time like '%"+log_time.strip()+"%'"
        if create_time:
          sql=sql+"  and create_time like '%"+create_time.strip()+"%'"
        offset = " ORDER BY ads_id DESC LIMIT {},{}".format(limit['page_index'] * limit['per_page'], limit['per_page'])
        datas = self.db_ads.execute(sql + offset).fetchall()
        lst = list()
        head=['identify_id', 'xhl_union_id', 'identify_name', 'identify_type', 'identify_card', 'country', 'sex', 'birthday', 'status', 'is_employee', 'phone_num', 'identify_img_front', 'identify_img_back', 'verify_status', 'log_time', 'create_time']
        for data in datas:
            temp = dict(zip(head, data))
            lst.append(temp)
        count = self.db_ads.execute("select count(*) from({}) as count_data".format(sql)).scalar()
        ret = self.set_page_params(count, limit, lst)
        self.write_json(0, data=ret)
        self.db_ads.close()


class UserIdentifyAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            identify_id = args["identify_id"]
            xhl_union_id = args["xhl_union_id"]
            identify_name = args["identify_name"]
            identify_type = args["identify_type"]
            identify_card = args["identify_card"]
            country = args["country"]
            sex = args["sex"]
            birthday = args["birthday"]
            status = args["status"]
            is_employee = args["is_employee"]
            phone_num = args["phone_num"]
            identify_img_front = args["identify_img_front"]
            identify_img_back = args["identify_img_back"]
            verify_status = args["verify_status"]
            log_time = args["log_time"]
            create_time = args["create_time"]
        useridentify = UserIdentify()
        useridentify.identify_id = identify_id
        useridentify.xhl_union_id = xhl_union_id
        useridentify.identify_name = identify_name
        useridentify.identify_type = identify_type
        useridentify.identify_card = identify_card
        useridentify.country = country
        useridentify.sex = sex
        useridentify.birthday = birthday
        useridentify.status = status
        useridentify.is_employee = is_employee
        useridentify.phone_num = phone_num
        useridentify.identify_img_front = identify_img_front
        useridentify.identify_img_back = identify_img_back
        useridentify.verify_status = verify_status
        useridentify.log_time = log_time
        useridentify.create_time = create_time
        self.db_ads.add(useridentify)
        try:
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()


class UserIdentifyDelHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        ids=None
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        if ids:
             self.db_ads.query(UserIdentify).filter(UserIdentify.id.in_(ids)).delete(synchronize_session=False)
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


class UserIdentifyEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        ids=None
        if args is not None:
            args = json.loads(args)
            id = args["id"]
            identify_id = args["identify_id"]
            xhl_union_id = args["xhl_union_id"]
            identify_name = args["identify_name"]
            identify_type = args["identify_type"]
            identify_card = args["identify_card"]
            country = args["country"]
            sex = args["sex"]
            birthday = args["birthday"]
            status = args["status"]
            is_employee = args["is_employee"]
            phone_num = args["phone_num"]
            identify_img_front = args["identify_img_front"]
            identify_img_back = args["identify_img_back"]
            verify_status = args["verify_status"]
            log_time = args["log_time"]
            create_time = args["create_time"]
        self.db_ads.query(UserIdentify).filter(UserIdentify.id == id).update({
            UserIdentify.identify_id: identify_id,
            UserIdentify.xhl_union_id: xhl_union_id,
            UserIdentify.identify_name: identify_name,
            UserIdentify.identify_type: identify_type,
            UserIdentify.identify_card: identify_card,
            UserIdentify.country: country,
            UserIdentify.sex: sex,
            UserIdentify.birthday: birthday,
            UserIdentify.status: status,
            UserIdentify.is_employee: is_employee,
            UserIdentify.phone_num: phone_num,
            UserIdentify.identify_img_front: identify_img_front,
            UserIdentify.identify_img_back: identify_img_back,
            UserIdentify.verify_status: verify_status,
            UserIdentify.log_time: log_time,
            UserIdentify.create_time: create_time,
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


{title: 'identify_id', key: 'identify_id',width: 30},
{title: 'xhl_union_id', key: 'xhl_union_id',width: 30},
{title: 'identify_name', key: 'identify_name',width: 30},
{title: 'identify_type', key: 'identify_type',width: 30},
{title: 'identify_card', key: 'identify_card',width: 30},
{title: 'country', key: 'country',width: 30},
{title: 'sex', key: 'sex',width: 30},
{title: 'birthday', key: 'birthday',width: 30},
{title: 'status', key: 'status',width: 30},
{title: 'is_employee', key: 'is_employee',width: 30},
{title: 'phone_num', key: 'phone_num',width: 30},
{title: 'identify_img_front', key: 'identify_img_front',width: 30},
{title: 'identify_img_back', key: 'identify_img_back',width: 30},
{title: 'verify_status', key: 'verify_status',width: 30},
{title: 'log_time', key: 'log_time',width: 30},
{title: 'create_time', key: 'create_time',width: 30},


class UserIdentify(Base):
    __tablename__ = "user_identify"
    identify_id = Column(Integer)
    xhl_union_id = Column(VARCHAR(255))
    identify_name = Column(VARCHAR(255))
    identify_type = Column()
    identify_card = Column(VARCHAR(255))
    country = Column(VARCHAR(255))
    sex = Column()
    birthday = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    status = Column()
    is_employee = Column()
    phone_num = Column()
    identify_img_front = Column(VARCHAR(255))
    identify_img_back = Column(VARCHAR(255))
    verify_status = Column()
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    create_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)



