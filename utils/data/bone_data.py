from typing import Self
from .serializable import Serializable
from .variant import Variant
from .collection_data import CollectionData
from ..bone_groups import vanilla_bones
from ..tools import is_bone_created
import bpy

class BoneData(Serializable):
    name: str
    visible: bool
    # bone_collections: list[str] | None
    bone_collections: CollectionData | None
    variants: dict[str, Variant]
    should_create: bool

    def __init__(self, name: str, visible: bool, bone_collections: CollectionData = None, should_create: bool = False) -> Self:
        self.name = name
        self.visible = visible
        self.bone_collections = bone_collections
        self.variants = {}
        self.should_create = should_create

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
        should_create = is_bone_created(bone.name, vanilla_bones)
        # bone_collections = [b.name for b in bbone.collections]
        bone_collections = CollectionData.from_bone(bone)
        return BoneData(name, visible, bone_collections, should_create)

    def serialize(self) -> dict:
        # Serialize the variants, excluding any that are empty or None
        serialized_variants = {k: v.serialize() for k, v in self.variants.items() if v and v.serialize()}

        # Construct the final dictionary, only including the variants if it's not empty
        serialized_data = {
            "name": self.name,
            "visible": self.visible,
            "should_create": self.should_create,
            "bone_collections": self.bone_collections.serialize()
        }

        # Only add the 'variants' key if the serialized variants dictionary is not empty
        if serialized_variants:
            serialized_data["variants"] = serialized_variants

        return serialized_data

    def deserialize(data) -> Self:
        collections = CollectionData.deserialize(data["bone_collections"])
        bone = BoneData(data["name"], data["visible"], collections, data["should_create"])
        if "variants" not in data:
            raise ValueError(f'Bone "${data["name"]}" has no Variant data.')
        for variant_name, variant_data in data["variants"].items():
            bone.variants[variant_name] = Variant.deserialize(variant_data)
        return bone
        