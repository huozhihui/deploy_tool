import ansible_api
import datetime, random


hosts = ["10.200.6.44","10.200.7.233"]
ext_vars = {"ansible_ssh_user": "root", "ansible_ssh_pass": "root"}
params = {"name": "user01", "state": "absent", "remove": "yes"}
dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
rand = random.randint(10, 99)
tid = "{dt}-{rand}".format(dt=dt, rand=rand)
ansible_api.api(tid, 'user', hosts, params, ext_vars)