import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n')
parser.add_argument('--type', '-t')
parser.add_argument('--generate', '-g', action=argparse.BooleanOptionalAction)
args = parser.parse_args()

if args.generate:
    if args.type not in ['manager', 'actions', 'auto']:
        raise ValueError('typeはmanagerかaction, autoのみを受け取ります')
    module_types = ['manager', 'actions'] if args.type == 'auto' else [args.type]

    split_name = args.name.split('/')
    path = '/'.join(split_name[:-1]) + '/'
    
    for module_type in module_types:
        if os.path.exists(f'../mipac/{module_type}/{path[:-1]}') is False:
            os.makedirs(f'../mipac/{module_type}/{path[:-1]}')
            with open(f'../mipac/{module_type}/{path}__init__.py', mode='w', encoding='utf-8') as f:
                f.close()
        with open(f'../mipac/{module_type}/{path}{split_name[-1]}.py', mode='w', encoding='utf-8') as f:
            f.close()
