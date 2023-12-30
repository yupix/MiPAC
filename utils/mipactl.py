import argparse
import os
from typing import Literal

from templates import (
    ACTIONS_CLASS_NAME_TEMPLATE,
    ACTIONS_TEMPLATE,
    MANAGER_CLASS_NAME_TEMPLATE,
    MANAGER_TEMPLATE,
)

ModuleTypes = Literal['manager', 'actions']

parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n')
parser.add_argument('--generate', '-g', action=argparse.BooleanOptionalAction)
args = parser.parse_args()


class Generator:
    def __init__(self) -> None:
        self.split_name = args.name.split('/')
        self.path = '/'.join(self.split_name[:-1]) + '/'
        self.base_path = '../mipac'

    def makedirs(self, module_type: ModuleTypes, path: str):
        if os.path.exists(f'../mipac/{module_type}/{path[:-1]}') is False:
            os.makedirs(f'../mipac/{module_type}/{path[:-1]}')
            with open(
                f'../mipac/{module_type}/{path}__init__.py', mode='w', encoding='utf-8'
            ) as f:
                f.close()

    def get_path(self, module_type: ModuleTypes):
        return f'{self.base_path}/{module_type}{self.path}{self.split_name[-1]}'

    def get_import_path(self, module_type: ModuleTypes):
        return self.get_path(module_type).replace('../', '').replace('/', '.')

    def get_class_name(self, module_type: ModuleTypes):
        return (
            MANAGER_CLASS_NAME_TEMPLATE
            if module_type == 'manager'
            else ACTIONS_CLASS_NAME_TEMPLATE
        ).format(self.split_name[-1].capitalize())

    def create_actions(self):
        import_path = self.get_import_path('actions')
        class_name = self.get_class_name('actions')
        os.makedirs(f'{self.base_path}/actions/{self.path}', exist_ok=True)
        with open(
            f'{self.base_path}/actions/{self.path}{self.split_name[-1]}.py',
            mode='w',
            encoding='utf-8',
        ) as f:
            f.write(ACTIONS_TEMPLATE.format(class_name))
            f.close()
        return {'import_path': import_path, 'class_name': class_name}

    def create_manager(self):
        created_actions = self.create_actions()
        class_name = self.get_class_name('manager')
        os.makedirs(f'{self.base_path}/manager/{self.path}', exist_ok=True)
        with open(
            f'{self.base_path}/manager/{self.path}{self.split_name[-1]}.py',
            mode='w',
            encoding='utf-8',
        ) as f:
            f.write(
                MANAGER_TEMPLATE.format(
                    class_name, created_actions['import_path'], created_actions['class_name']
                )
            )
            f.close()


if args.generate:
    module_types = ['manager', 'actions']

    generator = Generator()
    generator.create_manager()
