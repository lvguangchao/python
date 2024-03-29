#!/usr/bin/env python
# encoding: utf-8

"""
@author: lvguangchao
@email: guangchao.lv@qq.com
@time: 2018/1/17 15:53
"""
import pymysql


class AutoWriteCode(object):
    def __init__(self):
        self.col_type_map = {'int': "Integer", 'varchar': 'VARCHAR(255)',
                             'timestamp': 'DateTime(), default=datetime.now, onupdate=datetime.now',
                             'date': 'DateTime(), default=datetime.now, onupdate=datetime.now',
                             'datetime': 'DateTime(), default=datetime.now, onupdate=datetime.now',
                             'timestamp': 'DateTime(), default=datetime.now, onupdate=datetime.now',
                             'text': 'Text',
                             'numeric': 'Numeric',
                             }
        self.conn = pymysql.connect(host='192.168.120.84', port=3306, user='root', passwd='123456',
                                    db='xhl_withdraw')  # db：库名
        self.columns = None  # 表字段名称
        self.class_name = None
        self.table_name = None
        self.database_name = None

    def init(self,table_name,database_name):
        self.table_name = table_name
        self.database_name = database_name
        self.get_column_names(table_name,database_name)
        self.get_class_name(table_name)

    # 获取数据库字段，类型
    def get_column_names(self, table,database_name):
        cur = self.conn.cursor()
        cur.execute("SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA."
                    "columns WHERE TABLE_NAME='{}' and  table_schema='{}'".format(table,database_name))
        result = cur.fetchall()
        self.conn.commit()
        cur.close()
        self.conn.close()
        self.columns = [r for r in result]

    def get_class_name(self, table_name):
        names = table_name.split('_')
        class_name = ''
        for n in names:
            class_name += n.capitalize()
        self.class_name = class_name

    def write_table_class(self, ):
        with open(self.class_name + ".py", 'a') as f:
            f.write('class ' + self.class_name + "(Base):\n")
            f.write('    ' + '__tablename__ = "' + table_name + '"\n')
            for col in self.columns:
                col_name, col_type = col
                f.write('    ' + col_name + " = Column(" + self.col_type_map.get(col_type, '') + ")\n")
            f.write("\n")
            f.write("\n")
            f.write("\n")

    def write_select_class(self):
        with open(self.class_name + ".py", 'a', encoding='utf8') as f:
            f.write('class ' + self.class_name + "ListHander(SwxJsonHandler):\n")
            f.write('    ' + "@tornado.web.authenticated" + "\n")
            f.write('    ' + "def get(self, *args, **kwargs):" + "\n")
            f.write('    ' + '    ' + "self.render('')" + "\n")
            f.write('\n')
            f.write('    ' + "@tornado.web.authenticated" + "\n")
            f.write('    ' + "def post(self, *args, **kwargs):" + "\n")
            f.write('    ' + '    ' + "limit, args = self.get_pages_args()" + "\n")
            f.write('    ' + '    ' + "filter = args[\"filter\"]" + "\n")
            columns = []
            for col in self.columns:
                col_name, _ = col
                columns.append(col_name)
                f.write('    ' + '    ' + col_name + " = filter[\"" + col_name + "\"]" + "\n")

            sql = 'select ' + (','.join(columns)) + ' from ' + self.table_name + ' where 1=1'
            print(sql)
            f.write('    ' + '    sql="' + sql + '"\n')
            for col in self.columns:
                col_name, _ = col
                f.write('    ' + '    ' + 'if ' + col_name + ":\n")
                f.write(
                    '    ' + '    ' + '  ' + 'sql=sql+"  and ' + col_name + ' like \'%"+' + col_name + '.strip()' + '+"%\'"' + '\n')
            f.write(
                '    ' + '    ' + 'offset = " ORDER BY ads_id DESC LIMIT {},{}".format(limit[\'page_index\'] * limit[\'per_page\'], limit[\'per_page\'])' + '\n')
            f.write('    ' + '    ' + 'datas = self.db_ads.execute(sql + offset).fetchall()' + "\n")
            f.write('    ' + '    ' + 'lst = list()' + "\n")
            f.write('    ' + '    ' + 'head=' + str(columns) + "\n")
            f.write('    ' + '    ' + 'for data in datas' + ":\n")
            f.write('    ' + '    ' + '    ' + 'temp = dict(zip(head, data))' + "\n")
            f.write('    ' + '    ' + '    ' + 'lst.append(temp)' + "\n")
            f.write(
                '    ' + '    ' + 'count = self.db_ads.execute("select count(*) from({}) as count_data".format(sql)).scalar()' + "\n")
            f.write('    ' + '    ' + 'ret = self.set_page_params(count, limit, lst)' + "\n")
            f.write('    ' + '    ' + 'self.write_json(0, data=ret)' + "\n")
            f.write('    ' + '    ' + "self.db_ads.close()" + "\n")

            f.write("\n")
            f.write("\n")

    def write_add_class(self):
        with open(self.class_name + ".py", 'a', encoding='utf8') as f:
            f.write('class ' + self.class_name + 'AddHander(SwxJsonHandler):' + "\n")
            f.write('    ' + "@tornado.web.authenticated" + "\n")
            f.write('    ' + "@permision" + "\n")
            f.write('    ' + "def post(self, *args, **kwargs):" + "\n")
            f.write('    ' + '    ' + "args = self.get_argument('args', None)" + "\n")
            f.write('    ' + '    ' + "if args is not None:" + "\n")
            f.write('    ' + '    ' + '    ' + "args = json.loads(args)" + "\n")
            # columns = []
            for col in self.columns:
                col_name, _ = col
                # columns.append(col_name)
                f.write('    ' + '    ' + '    ' + col_name + " = args[\"" + col_name + "\"]" + "\n")

            f.write('    ' + '    ' + self.class_name.lower() + " = " + self.class_name + "()" + "\n")
            for col in self.columns:
                col_name, _ = col
                f.write('    ' + '    ' + self.class_name.lower() + "." + col_name + " = " + col_name + "\n")

            f.write('    ' + '    ' + "self.db_ads.add(" + self.class_name.lower() + ")\n")
            f.write('    ' + '    ' + "try:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.commit()" + "\n")
            f.write('    ' + '    ' + '    ' + "self.write_json(0)" + "\n")
            f.write('    ' + '    ' + "except Exception as e:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.rollback()" + "\n")
            f.write('    ' + '    ' + '    ' + "log.e(e)" + "\n")
            f.write('    ' + '    ' + '    ' + u"self.write_json(500, \"更新失败\")" + "\n")
            f.write('    ' + '    ' + "finally:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.close()" + "\n")
            f.write("\n")
            f.write("\n")

    def write_delete_class(self):
        with open(self.class_name + ".py", 'a', encoding='utf8') as f:
            f.write('class ' + self.class_name + 'DelHander(SwxJsonHandler):' + "\n")
            f.write('    ' + "@tornado.web.authenticated" + "\n")
            f.write('    ' + "@permision" + "\n")
            f.write('    ' + "def post(self, *args, **kwargs):" + "\n")
            f.write('    ' + '    ' + "args = self.get_argument('args', None)" + "\n")
            f.write('    ' + '    ' + "ids=None" + "\n")
            f.write('    ' + '    ' + "if args is not None:" + "\n")
            f.write('    ' + '    ' + '    ' + "args = json.loads(args)" + "\n")
            f.write('    ' + '    ' + '    ' + "ids = args[\"ids\"]" + "\n")
            f.write('    ' + '    ' + "if ids:" + "\n")
            f.write(
                '    ' + '    ' + '    ' + " self.db_ads.query(" + self.class_name + ").filter(" + self.class_name + ".id.in_(ids)).delete(synchronize_session=False)" + "\n")
            f.write('    ' + '    ' + "else:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.write(-1,'没有id')" + "\n")
            f.write('    ' + '    ' + '    ' + "return" + "\n")
            f.write('    ' + '    ' + "try:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.commit()" + "\n")
            f.write('    ' + '    ' + '    ' + "self.write_json(0)" + "\n")
            f.write('    ' + '    ' + "except Exception as e:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.rollback()" + "\n")
            f.write('    ' + '    ' + '    ' + "log.e(e)" + "\n")
            f.write('    ' + '    ' + '    ' + u"self.write_json(500, \"删除失败\")" + "\n")
            f.write('    ' + '    ' + "finally:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.close()" + "\n")
            f.write("\n")
            f.write("\n")

    def write_update_class(self):
        with open(self.class_name + ".py", 'a', encoding='utf8') as f:
            f.write('class ' + self.class_name + 'EditHander(SwxJsonHandler):' + "\n")
            f.write('    ' + "@tornado.web.authenticated" + "\n")
            f.write('    ' + "@permision" + "\n")
            f.write('    ' + "def post(self, *args, **kwargs):" + "\n")
            f.write('    ' + '    ' + "args = self.get_argument('args', None)" + "\n")
            f.write('    ' + '    ' + "ids=None" + "\n")
            f.write('    ' + '    ' + "if args is not None:" + "\n")
            f.write('    ' + '    ' + '    ' + "args = json.loads(args)" + "\n")
            f.write('    ' + '    ' + '    ' + "id = args[\"id\"]" + "\n")
            # columns = []
            for col in self.columns:
                col_name, _ = col
                # columns.append(col_name)
                f.write('    ' + '    ' + '    ' + col_name + " = args[\"" + col_name + "\"]" + "\n")

            f.write(
                '    ' + '    ' + "self.db_ads.query(" + self.class_name + ").filter(" + self.class_name + ".id == id).update({" + "\n")
            for col in self.columns:
                col_name, _ = col
                f.write('    ' + '    ' + '    ' + self.class_name + "." + col_name + ": " + col_name + "," "\n")
            f.write('    ' + '    ' + "})" + "\n")
            f.write('    ' + '    ' + "try:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.commit()" + "\n")
            f.write('    ' + '    ' + '    ' + "self.write_json(0)" + "\n")
            f.write('    ' + '    ' + "except Exception as e:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.rollback()" + "\n")
            f.write('    ' + '    ' + '    ' + "log.e(e)" + "\n")
            f.write('    ' + '    ' + '    ' + u"self.write_json(500, \"修改失败\")" + "\n")
            f.write('    ' + '    ' + "finally:" + "\n")
            f.write('    ' + '    ' + '    ' + "self.db_ads.close()" + "\n")
            f.write("\n")
            f.write("\n")

    def write_js_options(self):
        with open(self.class_name + ".py", 'a', encoding='utf8') as f:
            for col in self.columns:
                col_name, _ = col
                f.write("{title: '" + col_name + "', key: '" + col_name + "',width: 30},"+ "\n")
            f.write("\n")
            f.write("\n")


if __name__ == "__main__":
    table_name = 'user_identify'
    database_name = 'xhl_withdraw'
    code = AutoWriteCode()
    code.init(table_name,database_name)

    # 写table class
    code.write_select_class()
    code.write_add_class()
    code.write_delete_class()
    code.write_update_class()
    code.write_js_options()
    code.write_table_class()
