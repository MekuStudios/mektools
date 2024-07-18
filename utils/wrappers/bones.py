import bpy
import mathutils

from ..data import CustomShapeData
from ..tools import mode_set

class MBone:
    bone: bpy.types.Bone = None

    def __init__(self, bone: bpy.types.Bone) -> None:
        self.bone = bone


class MEditBone:
    bone: bpy.types.EditBone = None

    def __init__(self, bone: bpy.types.EditBone) -> None:
        self.bone = bone

class MPoseBone:
    bone: bpy.types.PoseBone = None

    def __init__(self, bone: bpy.types.PoseBone) -> None:
        self.bone = bone

    def set_custom_shape(self, custom_shape_object: bpy.types.Object,
                        custom_shape_data: CustomShapeData):
        with mode_set(mode="POSE"):
            self.bone.custom_shape = custom_shape_object
            self.bone.custom_shape_scale_xyz = custom_shape_data.scale
            self.bone.custom_shape_rotation_euler = custom_shape_data.rotation
            self.bone.custom_shape_translation = custom_shape_data.offset
            self.bone.color.palette = custom_shape_data.shape_color
    
    def set_visibility(self, visible: bool) -> None:
        with mode_set(mode="POSE"):
            self.bone.bone.hide = not visible;

    def toggle_visibility(self) -> bool:
        visible = False
        with mode_set(mode="POSE"):
            self.bone.bone.hide = not self.bone.bone.hide;
            visible = not self.bone.bone.hide
        return visible
