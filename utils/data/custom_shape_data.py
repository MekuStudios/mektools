from typing import Self
import bpy
from .serializable import Serializable

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
        for attr in attributes:
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
        