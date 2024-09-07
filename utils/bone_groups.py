import os

## ./Ensure YAML
import io, yaml # type: ignore
import itertools
from .tools import get_addon_absolute_path, flatten_nested_list



path_to_config = os.path.join(get_addon_absolute_path(), "bones.yaml")
with io.open(path_to_config) as stream:
    data = yaml.safe_load(stream)

data = {k.lower(): v for k, v in data.items()}
data = {k: list(flatten_nested_list(v)) for k,v in data.items()}
print(f'Loaded {len(data)} Bone Groups.')

vanilla_bones = list(set(itertools.chain.from_iterable(data.values())))
print(f'{len(vanilla_bones)} Vanilla Bones.')

path_to_config = os.path.join(get_addon_absolute_path(), "reference_bones.yaml")
with io.open(path_to_config) as stream:
    data2 = yaml.safe_load(stream)

data2 = {k.lower(): v for k, v in data2.items()}
data2 = {k: list(flatten_nested_list(v)) for k,v in data2.items()}
print(f'Loaded {len(data2)} Bone Groups.')
reference_bones = list(set(itertools.chain.from_iterable(data2.values())))
print(f'{len(vanilla_bones)} Reference Bones.')

