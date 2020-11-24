import converter
import json
from datetime import datetime
from event import Message


def _compare_service_lists(list1, list2):
    result_list = {
        'diff': [],
        'eq': [],
        'not': []
    }

    for s1 in list1:
        found = False
        for s2 in list2:
            if s1.name == s2.name:
                found = True
                if s1.startup == s2.startup:
                    result_list['eq'].append({
                        'name': s1.name,
                        'config': s1.startup,
                        'description': s1.description
                    })
                else:
                    result_list['diff'].append({
                        'name': s1.name,
                        'file1': s1.startup,
                        'file2': s2.startup
                    })
        if not found:
            result_list['not'].append({
                'name': s1.name,
                'file1': True,
                'file2': False
            })

    return result_list


# command
def diff_service_lists(args):
    path1 = converter.verify_path(args[0], [converter.CSV_SUFFIX,
                                            converter.XML_SUFFIX])
    path2 = converter.verify_path(args[1], [converter.CSV_SUFFIX,
                                            converter.XML_SUFFIX])

    s_list1 = converter.from_file(args[0], path1.suffix)
    s_list2 = converter.from_file(args[1], path2.suffix)

    use_list1_first = len(s_list1) > len(s_list2)
    # check the biggest list for logs services not found
    result = _compare_service_lists(s_list1, s_list2)\
        if use_list1_first\
        else _compare_service_lists(s_list2, s_list1)

    with open(r'./src/template.html', 'r') as f:
        res = ''.join(f.readlines())
        now = datetime.now()

        res = res.replace('[date]', now.strftime('%a %d %B, %Y %I:%M %p'))
        res = res.replace('[data]', json.dumps(result))  # dict to json str

        if (use_list1_first):
            res = res.replace('[file1]', path1.name)
            res = res.replace('[file2]', path2.name)
        else:
            res = res.replace('[file1]', path2.name)
            res = res.replace('[file2]', path1.name)

        with open(r'./output.html', 'w') as output:
            output.write(res)

    Message.create('''Diff completed!
                   You can check results openning the file "output.html"''',
                   Message.INFORMATION)
