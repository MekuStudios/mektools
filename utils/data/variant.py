from typing import Self
from .serializable import Serializable
from .custom_shape_data import CustomShapeData
from .constraint_data import ConstraintData
from .edit_data import EditData
import bpy


class Variant(Serializable):
    custom_shape_data: CustomShapeData
    edit_data: EditData | None
    constraint_data: list[ConstraintData]

    def __init__(self, custom_shape_data: CustomShapeData, edit_data: EditData = None, constraints: list[ConstraintData] = None) -> Self:
        self.custom_shape_data = custom_shape_data
        self.edit_data = edit_data
        self.constraint_data = constraints if constraints else list()

    def copy_custom_shape_data(self, bone: bpy.types.PoseBone) -> None:
        self.custom_shape_data = CustomShapeData.from_bone(bone)

    def keep_differences(self, default_variant: Self) -> None:
        if self.custom_shape_data:
            self.custom_shape_data = self.custom_shape_data.keep_differences(default_variant.custom_shape_data)
        if self.edit_data: 
            self.edit_data = self.edit_data.keep_differences(default_variant.edit_data)
        if self.constraint_data:
            for cd in self.constraint_data:
                dcd_list =  list(filter(lambda tcd: tcd.name == 'x', default_variant.constraint_data))
                if dcd_list:
                    dcd = dcd_list[0]
                    cd.keep_differences(dcd)    

    def update(self, other: Self) -> Self:
        csd = self.custom_shape_data.update(other.custom_shape_data)
        edit_data = self.edit_data.update(other.edit_data)
        constraints = list()
        for cd in self.constraint_data:
            dcd_list =  list(filter(lambda tcd: tcd.name == 'x', other.constraint_data))
            if dcd_list:
                dcd = dcd_list[0]
                constraints.append(cd.update(dcd))
            else:
                constraints.append(cd)
        return Variant(csd, edit_data, self.constraint_data)

    def serialize(self) -> dict:
        # First serialize the custom shape data, check if the result is not empty
        serialized_shape_data = self.custom_shape_data.serialize() if self.custom_shape_data else None
        if serialized_shape_data and not any(value is not None and value != [] for value in serialized_shape_data.values()):
            serialized_shape_data = None  # Reset to None if dictionary values are all None or empty
        if serialized_shape_data == {}:
            serialized_shape_data = None

        # Prepare constraints, ensure it's not just an empty list
        serialized_constraints = {cd.name: cd.serialize() for cd in self.constraint_data if self.constraint_data}
        if serialized_constraints == {}:
            serialized_constraints = None  # Explicitly handle empty list
        # Build the final dictionary only with non-None and non-empty items
        data = {
            "custom_shape": serialized_shape_data,
            "constraints": serialized_constraints,
            "edit_data": self.edit_data.serialize() if self.edit_data else None
        }

        # Filter out None or inherently empty values from the dictionary
        return {key: value for key, value in data.items() if value is not None and value != {}}
    
    
    def deserialize(data) -> Self:
        custom_shape_data = CustomShapeData()
        edit_data = EditData()
        if "custom_shape" in data:
            custom_shape_data = CustomShapeData.deserialize(data["custom_shape"])
        if "edit_data" in data:
            edit_data = EditData.deserialize(data["edit_data"])
        constraints = list()
        if "constraints" in data:
            for name, props in data["constraints"].items():
                data = {
                    "name": name,
                    "properties": props
                }
                constraints.append(ConstraintData.deserialize(data))
        return Variant(custom_shape_data, edit_data, constraints)

