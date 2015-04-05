## Function: To generate excel document
## Author: xiaoben
## Email: xiaoben@outlook.com
## Create Date:  2014-5-16
## Update Date: 2014-5-27 & 28: Optimize the code

import web
import model
import datetime
import mk_report

web.config.debug = True

### URL mappings
urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/viewall/(\d+)', 'ViewAll',
    '/new/(\d+)', 'New',
    '/del/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/download', 'Download',
    '/about', 'About',
    '/help', 'Help',
    '/sample_mgt', 'SampleManagement',
)

### Template
t_globals = { 
    
}

render = web.template.render('templates', base = 'base', globals = t_globals)


class Report:
    def __init__(self, who):
        self.who  = who
        self.job  = ''
        self.risk = ''
        self.plan = ''
        
    def add(self, job, risk, plan):
        self.job  = job
        self.risk = risk
        self.plan = plan

class Post:
    def __init__(self, username, userid, reportid=None, postdate=None):
        self.username = username
        self.userid   = userid
        self.reportid = reportid
        self.postdate = postdate

### memcache
g_memcachReport = []
g_memcachePost  = []
def initMemcachReport():
    pass
def initMemcachePost():
    pass
### memcache

class Index:
    def GET(self):
        '''Show home page'''
        users = model.get_users()
        posts = []
        for user in users:
            report = model.get_report_by_name(user.name)
            # bug??? Need ot konw the life scope of variable 'post' 
            if report != None:
                post = Post(user.name2, user.id, report.id, report.postdate)
            else:
                post = Post(user.name2, user.id)
            posts.append(post)
            
        today = datetime.date.today().strftime('%Y%m%d')
        return render.index(posts, today)

class View:
    def GET(self, id):
        '''View single report'''
        report = model.get_report_by_id(id)
        if report == None:
            raise web.seeother('/')
        return render.view(report)

class New:
    form = web.form.Form(
        web.form.Textarea('job', web.form.notnull,  rows = 8, cols = 80, description = 'JOB'),
        web.form.Textarea('risk', web.form.notnull, value='None', rows = 8, cols = 80, description = 'RISK'),
        web.form.Textarea('plan', web.form.notnull, rows = 8, cols = 80, description = 'PLAN'),
        # web.form.Button('Post', type = 'submit'), # don't forget to add 'type = submit'
        web.form.Button('Post', type = 'submit', class_='btn btn-success btn-sm'), # don't forget to add 'type = submit'
    )
    
    
    def GET(self, userid):
        today = datetime.date.today().strftime('%Y%m%d')
        form = self.form()
        return render.new(int(userid), form, today)

    def POST(self, userid):
        today = datetime.date.today().strftime('%Y%m%d')
        form = self.form()
        if not form.validates():
            return render.new(userid, form, today)

        user = model.get_user_by_id(userid)
        if user == None:
            raise web.seeother('/')

        model.new_report(form.d.job, form.d.risk, form.d.plan, user.name)
        raise web.seeother('/')

class Delete:
    def POST(self, reportid):
        model.del_report_by_id(int(reportid))
        raise web.seeother('/')

class Edit:
    form = web.form.Form(
        web.form.Textarea('job', web.form.notnull,  rows = 8, cols = 80, description = 'JOB'),
        web.form.Textarea('risk', web.form.notnull, rows = 8, cols = 80, description = 'RISK'),
        web.form.Textarea('plan', web.form.notnull, rows = 8, cols = 80, description = 'PLAN'),
        web.form.Button('Edit', type = 'submit', class_='btn btn-success btn-sm'), # don't forget to add 'type = submit'
    )
    def GET(self, reportid):
        form = self.form()
        report = model.get_report_by_id(int(reportid))
        if report == None:
            raise web.seeother('/')
        form.fill(report)
        return render.edit(report, form)

    def POST(self, reportid):
        form = self.form()
        if not form.validates():
            report = model.get_report_by_id(int(reportid))
            if report == None:
                raise web.seeother('/')
            return render.edit(report, form)
        model.update_report_by_id(int(reportid), form.d.job, form.d.risk, form.d.plan)
        raise web.seeother('/')

class Download:
    form = web.form.Form(
        web.form.Textarea('attend_staff', web.form.notnull, value= 'Yan Junping/Shen Junyong/Li Junjie/Chen Xuemei/Fan Yufeng/Zhou Xiaoyu/Zhang Jianhua/Yu Xuebiao/Gao Guiliang/Chen Jiaba/Lan Yuanheng/Lin Baoguang', rows = 5, cols = 80, description = 'Attend Staff'),
        web.form.Textbox('absent_staff', value='', size=77, description='Absent Staff'),
        web.form.Textbox('meeting_direct', web.form.notnull, value='Yan Junping', size=20, description='Meeting Direct'),
        web.form.Textbox('record_staff', web.form.notnull, value='Shen Junyong', size=20, description='Recordd Staff'),
        web.form.Button('Download', type = 'submit', class_='btn btn-success btn-sm'), # don't forget to add 'type = submit'
    )
    
    def GET(self):

        form = self.form()
        return render.download(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.download(form)

        root = 'file'
        filename = '(WeekReport)SW 3G5P Security TG_' + datetime.date.today().strftime('%Y%m%d') + '.xls'
        attend_staff = form.d.attend_staff
        absent_staff = form.d.absent_staff
        meeting_direct = form.d.meeting_direct
        record_staff = form.d.record_staff

        today_reports = list(model.get_all_reports())
        users = model.get_users()
        reports = []
        for user in users:
            report = Report(user.name)
            for tr in today_reports:
                if tr.who == user.name:
                    report.add(tr.job, tr.risk, tr.plan)
                    break
            # make sure that every user exist in the excel document even 
            # if it is emtpy
            reports.append(report) 
        
        issues = ''
        mk_report.generate_report(root, filename, attend_staff, absent_staff, meeting_direct, record_staff, reports, issues)
        
        # deal with download
        fd = file(root + '/' + filename, 'rb')
        # web.header('http-equiv', 'refresh') # redirect
        web.header('Content-type', 'application/octet-stream')
        fileinfo = 'attachment;filename="' + filename + '"'
        web.header('Content-Disposition', fileinfo)
        web.header('Content-transfer-encoding', 'binary')

        return fd.read()

class About:
    def GET(self):
        return render.about()

class Help:
    def GET(self):
        return render.help()

class SampleManagement:
    def GET(self):
        sample_ongoing_records = model.get_samples_ongoing()
        return render.sample_mgt(sample_ongoing_records)
        
        
def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.")

def internalerror():
    return web.internalerror("Bad, bad server. It seems has a error, please \
    come back later")

app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror
    
if __name__ == '__main__':
    app.run()
