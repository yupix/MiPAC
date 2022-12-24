pre = '''from .base import APIError


'''
template = '''class %sError(APIError):
    \"\"\" %s \"\"\"
'''


def error_name_to_hump(name: str) -> str:
    return ''.join([i.capitalize() for i in name.split('_')])


def gen_errors_py_files():
    with open('errors.csv', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.split('\n')[1:]

    error_list = {}
    for i in content:
        if i:
            i = i.split(',')
            error_list[i[0]] = i[1]

    all_content = [
        template % (error_name_to_hump(i), value)
        for i, value in error_list.items()
    ]

    with open('../../mipac/errors/errors.py', 'w', encoding='utf-8') as f:
        f.write(pre + '\n\n'.join(all_content))


if __name__ == '__main__':
    gen_errors_py_files()
    print('Done')
