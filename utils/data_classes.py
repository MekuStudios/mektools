from typing import Tuple, Union
from mathutils import Vector, Euler
from .bone_groups import vanilla_bones
import bpy

class Serializable:
    def __init__(self) -> None:
        pass
    
    def serialize(self) -> dict:
        raise NotImplementedError("This method should be implemented by subclasses")

class CustomShapeTransformData(Serializable):
    def __init__(self, variant_name: str, scale: list, offset: list, rotation: list) -> None:
        self.variant_name = variant_name
        # self.scale = scale
        # self.offset = offset
        self.scale = [item for sublist in (scale if isinstance(scale[0], (list, tuple)) else [scale]) for item in sublist]
        self.offset = [item for sublist in (offset if isinstance(offset[0], (list, tuple)) else [offset]) for item in sublist]
        self.rotation = rotation

    def serialize(self) -> dict:
        return {
            self.variant_name: {
                "scale": self.scale,
                "offset": self.offset,
                "rotation": self.rotation
            }
        }
        
class CustomShapeData(Serializable):
    transform_data: list[CustomShapeTransformData]

    def __init__(self, shape_name: str, shape_color: str) -> None:
        self.shape_name = shape_name
        self.shape_color = shape_color
        self.transform_data = list()
    
    def add_transform_data(self, data: CustomShapeTransformData) -> None:
        self.transform_data.append(data);

    def serialize(self) -> dict:
        transforms_dict = {}
        for data in self.transform_data:
            serialized = data.serialize()
            transforms_dict[data.variant_name] = serialized.get(data.variant_name)
        return {
            "name": self.shape_name,
            "color": self.shape_color,
            "transforms": transforms_dict
        }

class ConstraintData():
    def __init__(self, name: str) -> None:
        self.name = name

    def serialize(self):
        raise NotImplementedError("This method should be implemented by subclasses")

class BoneData(Serializable):
    name: str
    visible: bool
    is_vanilla_bone: bool
    custom_shape_data: CustomShapeData
    constraint_data: list[ConstraintData]

    def __init__(self, bone: bpy.types.PoseBone) -> None:
        self.name = bone.name
        self.visible = not bone.bone.hide
        self.is_vanilla_bone = True if bone.name in vanilla_bones else False
        self.constraint_data = list()

    def copy_custom_shape_data(self, bone: bpy.types.PoseBone) -> None:
        # Get Custom Shape Values
        scale=list(bone.custom_shape_scale_xyz),
        offset=list(bone.custom_shape_translation),
        rotation=list(bone.custom_shape_rotation_euler)
        cstd = CustomShapeTransformData("default", scale, offset, rotation)
        # Create Default Custom Shape Data data
        csd = CustomShapeData(shape_name=bone.custom_shape.name if bone.custom_shape else "None",
                                shape_color=bone.color.palette)
        csd.add_transform_data(cstd)
        # Copy to Bone Data
        self.custom_shape_data = csd

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "visible": self.visible,
            "is_vanilla_bone": self.is_vanilla_bone,
            "custom_shape": self.custom_shape_data.serialize() if self.custom_shape_data is not None else {},
            "constraints": [data.serialize() for data in self.constraint_data]
        }
