from django.core.management.base import BaseCommand, CommandError
from html import HTML
import os
import yaml


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        base_path = os.path.dirname(os.path.abspath(__file__))
        menu_path = os.path.join(base_path, 'g_menu', 'menu.html')
        yaml_path = os.path.join(base_path, 'g_menu', 'menu.yml')

        with open(yaml_path) as f:
            dataMap = yaml.load(f)

        print self.deal_date(dataMap)
        replacements = {'replace_menu': self.deal_date(dataMap)}
        with open(menu_path) as infile, open("templates/includes/menu.html", 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)



    def deal_date(self, date, level=1):
        s = ''
        for d in date:
            for k, v in d.items():
                s += self.child_menu(k, v, level)
        return s


    def child_menu(self, key, val, level=1):
        children = val.get('children', None)
        if children:
            level += 1
            s = self.deal_date(children, level)

        h = HTML()
        li = h.li(newlines=True)
        a = li.a(href=val['url'])
        klass = val.get('i_class', None)
        if klass is not None:
            a.i('', klass=klass)
        # t = "{% trans '" + key + "' %}"
        name = val.get('name', '')
        print "aaaaa"
        print name
        a.text(name)
        children = val.get('children', None)
        if children is not None:
            a.span(klass="fa arrow")

        if children:
            ul = li.ul(klass="nav nav-second-level", newlines=True)
            ul.text(s, escape=False)
        return str(h)
