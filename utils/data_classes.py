from typing import Self, Tuple, Union
from mathutils import Vector, Euler
from .bone_groups import vanilla_bones
import bpy

class Serializable:
    def __init__(self) -> Self:
        pass
    
    def serialize(self) -> dict:
        raise NotImplementedError("This method should be implemented by subclasses")

    def deserialize(data) -> Self:
        raise NotImplementedError("This method should be implemented by subclasses")

class CustomShapeData(Serializable):
    def __init__(self, shape_name: str = None, shape_color: str = None, scale: list = None,
                offset: list = None, rotation: list = None) -> Self:
        self.shape_name = shape_name
        self.shape_color = shape_color
        if scale:
            self.scale = [item for sublist in (scale if isinstance(scale[0], (list, tuple)) else [scale]) for item in sublist]
        else: 
            self.scale = None
        if offset:
            self.offset = [item for sublist in (offset if isinstance(offset[0], (list, tuple)) else [offset]) for item in sublist]
        else: self.offset = None
        self.rotation = rotation if rotation is not None else None


    def from_bone(bone: bpy.types.PoseBone) -> Self:
        shape_name=bone.custom_shape.name if bone.custom_shape else "None"
        shape_color=bone.color.palette
        if bone.custom_shape:
            scale=list(bone.custom_shape_scale_xyz),
            offset=list(bone.custom_shape_translation),
            rotation=list(bone.custom_shape_rotation_euler)
        else:
            scale = []
            offset = []
            rotation = []
        
        return CustomShapeData(shape_name, shape_color, scale, offset, rotation)

    def keep_differences(self, default_custom_shape_data: Self) -> Self:
         # Create a dictionary to hold the new attributes for the resultant instance
        new_attrs = {}

        # List of attributes to check
        attributes = ['shape_name', 'shape_color', 'scale', 'offset', 'rotation']

        # Compare each attribute of the current instance (self) with the other instance
        for attr in attributes:
            value1 = getattr(self, attr, None)
            value2 = getattr(default_custom_shape_data, attr, None)

            # If both values are lists, compare their contents
            if isinstance(value1, list) and isinstance(value2, list):
                # Check if lists are different, store only differences or None if they are the same
                new_attrs[attr] = value1 if value1 != value2 else None
            else:
                # Store the attribute value from self if it differs, else store None
                new_attrs[attr] = value1 if value1 != value2 else None

        # Create and return a new instance of MyClass using the computed differences
        return CustomShapeData(**new_attrs)

    def update(self, other: Self) -> Self:
        # List of attributes to check
        attributes = ['shape_name', 'shape_color', 'scale', 'offset', 'rotation']

        # Create a dictionary to hold new attribute values
        new_attrs = {}
        
        # Get current values as a base, to ensure all attributes are included
        for attr in ['shape_name', 'shape_color', 'scale', 'offset', 'rotation']:
            new_attrs[attr] = getattr(self, attr)

        # Apply updates from 'other' where applicable
        for attr in attributes:
            new_value = getattr(other, attr, None)
            if new_value is not None:
                new_attrs[attr] = new_value

        # Create a new instance with combined attributes
        return CustomShapeData(**new_attrs)

    def serialize(self) -> dict:
        # Build a complete dictionary including all attributes
        complete_data = {
            "name": self.shape_name,
            "color": self.shape_color,
            "scale": self.scale,
            "offset": self.offset,
            "rotation": self.rotation
        }

        # Filter out any keys that have None values
        filtered_data = {key: value for key, value in complete_data.items() if value is not None}

        # Organize data to nest scale, offset, and rotation under 'transforms' if any are present
        if any(k in filtered_data for k in ["scale", "offset", "rotation"]):
            filtered_data["transforms"] = {
                key: filtered_data.pop(key) for key in ["scale", "offset", "rotation"] if key in filtered_data
            }

        return filtered_data

    def deserialize(data) -> Self:
        # Retrieve 'transforms' safely, default to an empty dictionary if missing
        transforms = data.get('transforms', {})

        # Retrieve transformation data, default to None if not provided
        scale = transforms.get('scale', None)
        offset = transforms.get('offset', None)
        rotation = transforms.get('rotation', None)

        # Retrieve 'name' and 'color', default to None if not provided
        name = data.get('name', None)
        color = data.get('color', None)

        return CustomShapeData(shape_name=name, shape_color=color,scale=scale,
                            offset=offset, rotation=rotation)
        

class ConstraintData():
    def __init__(self, name: str) -> Self:
        self.name = name

    def serialize(self):
        raise NotImplementedError("This method should be implemented by subclasses")

class Variant(Serializable):
    custom_shape_data: CustomShapeData
    constraint_data: list[ConstraintData]

    def __init__(self, custom_shape_data: CustomShapeData) -> Self:
        self.custom_shape_data = custom_shape_data
        self.constraint_data = list()

    def copy_custom_shape_data(self, bone: bpy.types.PoseBone) -> None:
        self.custom_shape_data = CustomShapeData.from_bone(bone)

    def keep_differences(self, default_variant: Self) -> None:
        self.custom_shape_data = self.custom_shape_data.keep_differences(default_variant.custom_shape_data)
        # TODO: Constraint Diff

    def update(self, other: Self) -> Self:
        csd = self.custom_shape_data.update(other.custom_shape_data)
        print(csd.serialize())
        # TODO: Constraint Update
        return Variant(csd)

    def serialize(self) -> dict:
        # First serialize the custom shape data, check if the result is not empty
        serialized_shape_data = self.custom_shape_data.serialize() if self.custom_shape_data else None
        if serialized_shape_data and not any(value is not None and value != [] for value in serialized_shape_data.values()):
            serialized_shape_data = None  # Reset to None if dictionary values are all None or empty
        if serialized_shape_data == {}:
            serialized_shape_data = None

        # Prepare constraints, ensure it's not just an empty list
        serialized_constraints = self.constraint_data if self.constraint_data else None
        if serialized_constraints == []:
            serialized_constraints = None  # Explicitly handle empty list

        # Build the final dictionary only with non-None and non-empty items
        data = {
            "custom_shape": serialized_shape_data,
            "constraints": serialized_constraints
        }

        # Filter out None or inherently empty values from the dictionary
        return {key: value for key, value in data.items() if value is not None and value != []}
    
    
    def deserialize(data) -> Self:
        custom_shape_data = CustomShapeData.deserialize(data["custom_shape"])
        return Variant(custom_shape_data)

class BoneData(Serializable):
    name: str
    visible: bool
    is_vanilla_bone: bool
    variants: dict[str, Variant]

    def __init__(self, name: str, visible: bool, is_vanilla: bool) -> Self:
        self.name = name
        self.visible = visible
        self.is_vanilla_bone = is_vanilla
        self.variants = {}

    def get_variant(self, variant_name: str) -> Variant:
        default_variant: Variant = self.variants["default"]
        if variant_name == "default": return default_variant
        if variant_name in self.variants: 
            variant: Variant = self.variants[variant_name]
            return default_variant.update(variant)
        else:
            return default_variant
    
    def add_variant(self, variant: Variant, variant_name: str = "default",
                    overwrite: bool = False) -> Variant:
        if variant_name == "default":
            self.variants[variant_name] = variant
            return variant
        if variant_name in self.variants and overwrite == False:
            raise ValueError("Variant Name already in use.")
        
        # Grab Default Variant
        default_variant = self.variants["default"]
        # Keep only different values and add variant to dict
        variant.keep_differences(default_variant)
        self.variants[variant_name] = variant

    def from_bone(bone: bpy.types.PoseBone = None) -> Self:
        name = bone.name
        visible = not bone.bone.hide
        is_vanilla_bone = True if bone.name in vanilla_bones else False
        return BoneData(name, visible, is_vanilla_bone)

    def serialize(self) -> dict:
        # Serialize the variants, excluding any that are empty or None
        serialized_variants = {k: v.serialize() for k, v in self.variants.items() if v and v.serialize()}

        # Construct the final dictionary, only including the variants if it's not empty
        serialized_data = {
            "name": self.name,
            "visible": self.visible,
            "is_vanilla_bone": self.is_vanilla_bone
        }

        # Only add the 'variants' key if the serialized variants dictionary is not empty
        if serialized_variants:
            serialized_data["variants"] = serialized_variants

        return serialized_data

    def deserialize(data) -> Self:
        bone = BoneData(data["name"], data["visible"], data["is_vanilla_bone"])
        for variant_name, variant_data in data["variants"].items():
            bone.variants[variant_name] = Variant.deserialize(variant_data)
        return bone
        # for constraint in data["constraints"]:
        #     bone.constraint_data.append()
        
    

