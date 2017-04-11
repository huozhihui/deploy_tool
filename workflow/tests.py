from django.test import TestCase
import yaml
import os


def test_yml_step_count(yml_path):
    with open(yml_path, 'r+') as f:
        data = yaml.load(f)
        roles = data[0].get('roles', None)
        step_count = 0
        if roles:
            for role in roles:
                role_yaml_path = os.path.join('./roles', role, 'tasks/main.yml')
                with open(role_yaml_path, 'r+') as rf:
                    for d in yaml.load(rf):
                        if d.get('name', None):
                                print d.get('name', None)
                                step_count += 1
                print step_count
        else:
            tasks = data[0].get('tasks', None)
            for d in tasks:
                if d.get('name', None):
                        step_count += 1
            print tasks
            #step_count += len(tasks)
    return step_count
print "result"
print test_yml_step_count('userimage_install.yml')