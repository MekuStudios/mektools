from typing import Self

from .serializable import Serializable
from ..config import data as config
import bpy


class ConstraintData(Serializable):
    name: str = None
    properties: dict = None

    def __init__(self, name: str, properties: dict) -> Self:
        self.name = name
        self.properties = properties

    def create(self, bone: bpy.types.PoseBone, armature: bpy.types.Object) -> None:
        # Setup the constraints
        constraint: bpy.types.Constraint = bone.constraints.new(type=self.properties["type"])
        constraint.name = self.name
        for prop_name, prop_value in self.properties.items():
            if prop_name == "type": continue
            if isinstance(prop_value, str) and prop_value.startswith("obj."):
                obj_name = prop_value.replace("obj.", "")
                if obj_name == config["armature_constraint_name_placeholder"]:
                    value = armature
                else:
                    value = bpy.data.objects.get(obj_name)
                setattr(constraint, prop_name, value)
            else:
                setattr(constraint, prop_name, prop_value)
        # NOTE: This isn't a great fix, but the bug is stupid so ohwell
        if bone.name == "IK_Leg_Pole.R" and "Child Of" in constraint.name:
            constraint.set_inverse_pending = True
        if bone.name == "IK_Leg_Pole.L" and "Child Of" in constraint.name:
            constraint.set_inverse_pending = True

    def from_constraint(constraint: bpy.types.Constraint, armature: bpy.types.Object) -> Self:
        cname = constraint.name
        cprops = {}
        
        # Collect properties based on constraint type
        props = [p.identifier for p in constraint.bl_rna.properties if not p.is_readonly]
        for prop in props:
            if prop.startswith("__"):
                continue  # Skip dunder properties

            value = getattr(constraint, prop, None)
            # Check if the value is one of the serializable types
            if isinstance(value, (float, int, str, bool)):
                cprops[prop] = value
            if isinstance(value, (bpy.types.Object)):
                if value.name == armature.data.name:
                    cprops[prop] = "obj." + config["armature_constraint_name_placeholder"]
                else:
                    cprops[prop] = "obj." + value.name
        cprops["type"] = constraint.type
        return ConstraintData(cname, cprops)

    def keep_differences(self, other: Self) -> Self:
         # Create a dictionary to hold the new attributes for the resultant instance
        new_props = {}

        # List of attributes to check
        attributes = self.properties.keys()

        # Compare each attribute of the current instance (self) with the other instance
        for attr in attributes:
            value1 = self.properties.get(attr, None)
            value2 = other.properties.get(attr, None)

            # If both values are lists, compare their contents
            if isinstance(value1, list) and isinstance(value2, list):
                # Check if lists are different, store only differences or None if they are the same
                new_props[attr] = value1 if value1 != value2 else None
            else:
                # Store the attribute value from self if it differs, else store None
                new_props[attr] = value1 if value1 != value2 else None

        # Create and return a new instance of MyClass using the computed differences
        return ConstraintData(self.name, new_props)

    def update(self, other: Self) -> Self:
        # List of attributes to check
        attributes = self.properties.keys()

        # Create a dictionary to hold new attribute values
        new_props = {}
        
        # Get current values as a base, to ensure all attributes are included
        for attr in attributes:
            new_props[attr] = self.properties.get(attr, None)

        # Apply updates from 'other' where applicable
        for attr in attributes:
            new_value = other.get(attr, None)
            if new_value is not None:
                new_props[attr] = new_value

        # Create a new instance with combined attributes
        return ConstraintData(self.name, new_props)

    def serialize(self) -> dict:
        constraint_detail = {}
         # Format
        for prop, value in self.properties.items():
            constraint_detail[prop] = value
        return constraint_detail
    
    def deserialize(data) -> Self:
        return ConstraintData(name=data.get("name", None), properties=data.get("properties", None))