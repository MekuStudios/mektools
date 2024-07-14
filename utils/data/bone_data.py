from typing import Self
from .serializable import Serializable
from .variant import Variant
from ..bone_groups import vanilla_bones
import bpy

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
        