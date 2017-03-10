import yaml
import os

class OperateHost:
    def __init__(self):
        self.path = "hosts"

    def rw_host_file(self):
        pass

    def w_host_file(self, group, content):
        data = dict(

            A='a',
            B=dict(
                C='c',
                D='d',
                E='e',
            )
        )
        with open(self.path, 'w') as outfile:
            yaml.dump(date, outfile, default_flow_style=True)
        print outfile

    def host_file_exist(self):
        if not os.path.exists(self.path):
            pass


if __name__ == '__main__':
    h = OperateHost()
    print h.host_file_exist()

# with open('data.yml', 'r+') as f:
#     date = yaml.load(f)
#     tasks = date[0]['tasks']
#     print date
#     date[0]['hosts'] = '10.200.7.233'
#     date[0]['vars']['username'] = 'test'
#     dict = {'home': '/root', 'shell': '/bin/bash'}
#     for k, v in dict.iteritems():
#         tasks[0]['user'][k] = v
#     print date
#     yaml.dump(date, f)