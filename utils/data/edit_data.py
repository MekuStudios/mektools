from typing import Self
from .serializable import Serializable
from ..bone_groups import vanilla_bones
from ..tools import mode_set
from mathutils import Vector
import bpy

class EditData(Serializable):

    def __init__(self, head_offset: tuple[float, float, float] = None,
                 tail_offset: tuple[float, float, float] = None, roll: float = None,
                 parent_name: str = None, use_connect: bool = None, nearest_neighboor_head_name: str = None,
                 nearest_neighboor_tail_name: str = None) -> Self:
        self.head_offset = head_offset
        self.tail_offset = tail_offset
        self.roll = roll
        self.parent_name = parent_name
        self.use_connect = use_connect
        self.nearest_neighboor_head_name = nearest_neighboor_head_name
        self.nearest_neighboor_tail_name = nearest_neighboor_tail_name
    
    def from_bone(bone: bpy.types.EditBone, nn_head: dict, nn_tail: dict) -> Self:
        nvb_head = Vector(nn_head["bone"].head if nn_head["head"] is True else nn_head["bone"].tail)
        nvb_tail = Vector(nn_tail["bone"].head if nn_tail["head"] is True else nn_tail["bone"].tail)
        head = Vector(bone.head)
        tail = Vector(bone.tail)
        head_offset = list(head - nvb_head)
        tail_offset = list(tail - nvb_tail)
        roll = bone.roll
        parent = bone.parent.name if bone.parent else None
        use_connect = bone.use_connect
        nearest_neighboor_head_name = ">>".join([nn_head["bone"].name, ("head" if nn_head["head"] else "tail")])
        nearest_neighboor_tail_name = ">>".join([nn_tail["bone"].name, ("head" if nn_tail["head"] else "tail")])

        return EditData(head_offset, tail_offset, roll, parent, use_connect, nearest_neighboor_head_name, nearest_neighboor_tail_name)
        

    def create(self, armature: bpy.types.Object, bone_name: str, existing_bones: dict) -> None:
        if bone_name in existing_bones: return
        nn_head_name = self.nearest_neighboor_head_name.split(">>")[0]
        nn_tail_name = self.nearest_neighboor_tail_name.split(">>")[0]
        nn_head_side = self.nearest_neighboor_head_name.split(">>")[1]
        nn_tail_side = self.nearest_neighboor_tail_name.split(">>")[1]

        nn_head: bpy.types.EditBone = armature.data.edit_bones.get(nn_head_name)
        nn_tail: bpy.types.EditBone = armature.data.edit_bones.get(nn_tail_name)
        if not nn_head or not nn_tail: 
            return print("Couldn't find Vanilla bones for '"+bone_name+"'.")
        new_bone: bpy.types.EditBone = armature.data.edit_bones.new(bone_name)
        new_bone.head = (nn_head.head if nn_head_side == "head" else nn_head.tail) + Vector(self.head_offset)
        new_bone.tail = (nn_tail.head if nn_tail_side == "head" else nn_tail.tail) + Vector(self.tail_offset)
        new_bone.roll = self.roll
        
    def connect(self, armature: bpy.types.Object, bone_name: str, existing_bones: dict) -> None:
        if self.parent_name and self.parent_name in existing_bones:
            bone = armature.data.edit_bones.get(bone_name)
            bone.parent = armature.data.edit_bones.get(self.parent_name)
            bone.use_connect = self.use_connect

    def keep_differences(self, other: Self) -> Self:
         # Create a dictionary to hold the new attributes for the resultant instance
        new_attrs = {}

        attributes = ['head_offset', 'tail_offset', 'roll', 'parent_name', 'use_connect', 'nearest_neighboor_head_name', 'nearest_neighboor_tail_name']
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
        attributes = ['head_offset', 'tail_offset', 'roll', 'parent_name', 'use_connect', 'nearest_neighboor_head_name', 'nearest_neighboor_tail_name']

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
            "nearest_neighboor_head_name": self.nearest_neighboor_head_name,
            "nearest_neighboor_tail_name": self.nearest_neighboor_tail_name
        }

        # Filter out any keys that have None values
        return {key: value for key, value in complete_data.items() if value is not None}
        
    def deserialize(data) -> Self:
        head_offset = data.get('head_offset', None)
        tail_offset = data.get('tail_offset', None)
        roll = data.get('roll', None)
        parent = data.get('parent_name', None)
        use_connect = data.get('use_connect', None)
        nearest_neighboor_head_name = data.get('nearest_neighboor_head_name', None)
        nearest_neighboor_tail_name = data.get('nearest_neighboor_tail_name', None)
        return EditData(head_offset, tail_offset, roll, parent, use_connect, nearest_neighboor_head_name, nearest_neighboor_tail_name)
