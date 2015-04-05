import web

db = web.database(dbn='sqlite', db = 'wrs.db')

user_names = ['Yan Junping', 'Li Junjie', 'Chen Xuemei', 'Fan Yufeng', 'Zhou Xiaoyu', 'Zhang Jianhua', 'Yu Xuebiao', 'Gao Guiliang', 'Chen Jiaba', 'Lan Yuangheng', 'Lin Baoguang', 'Shen Junyong']

for name in user_names:
    db.insert('user', single_id = '', name = name)
