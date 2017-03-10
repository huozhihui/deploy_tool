class Person:
    template_name = "person template name"
    #def template_name(self):
    #    return "{0}/index.html".format(self._class_name())

class Child(Person):
    def _class_name(self):
        return "child"

class Children(Person):
    def _class_name(self):
        return "children"
    

class Childr(Person):
    def _class_name(self):
        return "childr"
    def template_name(self):
        return "{0}/index_two.html".format(self._class_name())

child = Child()
print child.template_name()
children = Children()
print children.template_name()
childr = Childr()
print childr.template_name()
