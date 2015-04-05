import web
import datetime
import time
import datetime

db = web.database(dbn='sqlite', db='wrg.db')


def get_users():
    return db.select('user')


def get_user_by_id(id):
    try:
        return db.select('user', where='id=$id', vars=locals())[0]
    except IndexError:
        return None


def get_all_reports():
    return db.select('report', order='id DESC')


def get_today_reports():
    today = datetime.date.today().strftime('%Y%m%d')
    try:
        return db.select('report', where='postdate=$today', vars=locals())
    except IndexError:
        return None


def get_report_by_name(name):
    try:
        return db.select('report', order='id DESC', where='who=$name', vars=locals())[0]
    except IndexError:
        return None


def get_report_by_id(id):
    try:
        return db.select('report', order='id DESC', where='id=$id', vars=locals())[0]
    except IndexError:
        return None


def new_report(job, risk, plan, who):
    #db.insert('report', job = job, risk = risk, plan = plan, postdate = time.asctime())
    _today = datetime.date.today()
    _postdate = _today.strftime('%Y%m%d')
    db.insert('report', job=job, risk=risk,
              plan=plan, postdate=_postdate, who=who)


def del_report_by_id(id):
    db.delete('report', where='id=$id', vars=locals())


def update_report_by_id(id, job, risk, plan):
    _today = datetime.date.today()
    _postdate = _today.strftime('%Y%m%d')
    db.update('report', where='id=$id', vars=locals(), job=job,
              risk=risk, plan=plan, postdate=_postdate)
