from typing import Self
from .serializable import Serializable
from ..bone_groups import vanilla_bones
from ..tools import mode_set
from mathutils import Vector
import bpy

class EditData(Serializable):

    def __init__(self, head_offset: tuple[float, float, float] = None,
                 tail_offset: tuple[float, float, float] = None, roll: float = None,
                 parent_name: str = None, use_connect: bool = None, nearest_neighboor_name: str = None) -> Self:
        self.head_offset = head_offset
        self.tail_offset = tail_offset
        self.roll = roll
        self.parent_name = parent_name
        self.use_connect = use_connect
        self.nearest_neighboor_name = nearest_neighboor_name
    
    def from_bone(bone: bpy.types.EditBone, nearest_vanilla_bone: bpy.types.EditBone) -> Self:
        nvb_head = Vector(nearest_vanilla_bone.head)
        head = Vector(bone.head)
        tail = Vector(bone.tail)
        head_offset = list(head - nvb_head)
        tail_offset = list(tail - nvb_head)
        roll = bone.roll
        parent = bone.parent.name if bone.parent else None
        use_connect = bone.use_connect
        nearest_neighboor_name = nearest_vanilla_bone.name

        return EditData(head_offset, tail_offset, roll, parent, use_connect, nearest_neighboor_name)
        

    def create(self, armature: bpy.types.Object, bone_name: str, existing_bones: dict) -> None:
        if bone_name in existing_bones: return
        nearest_bone: bpy.types.EditBone = armature.data.edit_bones.get(self.nearest_neighboor_name)
        if not nearest_bone: 
            raise ValueError("Couldn't find Vanilla bone '"+self.nearest_neighboor_name+"'.")
        new_bone: bpy.types.EditBone = armature.data.edit_bones.new(bone_name)
        new_bone.head = nearest_bone.head + Vector(self.head_offset)
        new_bone.tail = nearest_bone.head + Vector(self.tail_offset)
        new_bone.roll = self.roll
        
    def connect(self, armature: bpy.types.Object, bone_name: str, existing_bones: dict) -> None:
        if self.parent_name and self.parent_name in existing_bones:
            bone = armature.data.edit_bones.get(bone_name)
            bone.parent = armature.data.edit_bones.get(self.parent_name)
            bone.use_connect = self.use_connect

    def keep_differences(self, other: Self) -> Self:
         # Create a dictionary to hold the new attributes for the resultant instance
        new_attrs = {}

        attributes = ['head_offset', 'tail_offset', 'roll', 'parent_name', 'use_connect', 'nearest_neighboor_name']
        # Compare each attribute of the current instance (self) with the other instance
        for attr in attributes:
            value1 = getattr(self, attr, None)
            value2 = getattr(other, attr, None)

            # If both values are lists, compare their contents
            if isinstance(value1, list) and isinstance(value2, list):
                # Check if lists are different, store only differences or None if they are the same
                new_attrs[attr] = value1 if value1 != value2 else None
            else:
                # Store the attribute value from self if it differs, else store None
                new_attrs[attr] = value1 if value1 != value2 else None

        # Create and return a new instance of MyClass using the computed differences
        return EditData(**new_attrs)

    def update(self, other: Self) -> Self:
        # List of attributes to check
        attributes = ['head_offset', 'tail_offset', 'roll', 'parent_name', 'use_connect', 'nearest_neighboor_name']

        # Create a dictionary to hold new attribute values
        new_attrs = {}
        
        # Get current values as a base, to ensure all attributes are included
        for attr in attributes:
            new_attrs[attr] = getattr(self, attr)

        # Apply updates from 'other' where applicable
        for attr in attributes:
            new_value = getattr(other, attr, None)
            if new_value is not None:
                new_attrs[attr] = new_value

        # Create a new instance with combined attributes
        return EditData(**new_attrs)

    def serialize(self) -> dict:
        # Build a complete dictionary including all attributes
        complete_data = {
            "head_offset": self.head_offset,
            "tail_offset": self.tail_offset,
            "roll": self.roll,
            "parent_name": self.parent_name,
            "use_connect": self.use_connect,
            "nearest_neighboor_name": self.nearest_neighboor_name
        }

        # Filter out any keys that have None values
        return {key: value for key, value in complete_data.items() if value is not None}
        
    def deserialize(data) -> Self:
        head_offset = data.get('head_offset', None)
        tail_offset = data.get('tail_offset', None)
        roll = data.get('roll', None)
        parent = data.get('parent_name', None)
        use_connect = data.get('use_connect', None)
        nearest_neighboor_name = data.get('nearest_neighboor_name', None)
        return EditData(head_offset, tail_offset, roll, parent, use_connect, nearest_neighboor_name)
