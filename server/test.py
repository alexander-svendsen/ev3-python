# -*- coding: utf-8 -*-
import inspect

from behaviors.subsumption import Behavior, Controller
behavior = 'a = 1 \nclass SomeBehaviorName(Behavior):' + '\n\tdef check(self):' + '\n\t\tprint a' + '\n\tdef action(self):' + '\n\t\tpass' + '\n\tdef suppress(self):' + '\n\t\tpass'
print_test = 'def foo(): \n\tprint "mordi"'
expression_dict = {'Behavior': Behavior}


default_dict = {'Behavior': Behavior}
exec '' in default_dict
exec behavior in expression_dict

behavior_set = set(expression_dict) - set(default_dict)
for instance in behavior_set:
    if inspect.isclass(expression_dict[instance]):
        print instance


module = {'name': expression_dict['SomeBehaviorName']}
print module['name']()
# a = expression_dict['SomeBehaviorName']()
# print expression_dict
# expression_dict.foo()
# b = SomeBehaviorName()
# b.check()