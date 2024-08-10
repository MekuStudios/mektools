from typing import Self
from .serializable import Serializable
from ..bone_groups import vanilla_bones
from ..tools import mode_set
import bpy

class CollectionData(Serializable):

    def __init__(self, collections: list[dict]) -> Self:
        self.collections = collections
        pass

    def from_bone(bone: bpy.types.PoseBone) -> Self:
        collections: list = []
        bbone: bpy.types.Bone = bone.bone
        for b in bbone.collections:
            collections.append(CollectionData.form_collection_dict(b))
        return CollectionData(collections)
    
    def create_and_attach(self, armature: bpy.types.Armature, bone: bpy.types.Bone) -> None:
        CollectionData.create_collections(self.collections, armature)
        for col in self.collections:
            collection_name = col["name"];
            with mode_set(mode="POSE"):
                armature.collections_all[collection_name].assign(bone)

    def create_collections(collections: list[dict], armature: bpy.types.Armature) -> bpy.types.BoneCollection:
        col = None
        for collection in collections:
            name = collection["name"]
            is_visible = collection["is_visible"]
            parent_data = collection.get("parent", None)

            if parent_data:
                parent_name = parent_data["name"]
                if parent_name not in armature.collections_all:
                    parent_collection: bpy.types.BoneCollection = CollectionData.create_collections([parent_data], armature)
                else:
                    parent_collection: bpy.types.BoneCollection = armature.collections_all[parent_name]
            else:
                parent_collection = None

            col = CollectionData.create_collection(armature, name, is_visible, parent_collection)
        
        return col

    def create_collection(armature: bpy.types.Armature, collection_name: str, is_visible: bool,
                        parent_collection: bpy.types.BoneCollection | None = None):
        # Check if collection already exists
        if collection_name in armature.collections_all:
            collection: bpy.types.BoneCollection = armature.collections_all[collection_name]
        else:
            collection: bpy.types.BoneCollection = armature.collections.new(collection_name)
        
        collection.is_visible = is_visible

        if parent_collection and parent_collection.name in armature.collections_all:
            parent_coll: bpy.types.BoneCollection = armature.collections_all[parent_collection.name]
            collection.parent = parent_coll

        return collection

    def form_collection_dict(col: bpy.types.BoneCollection) -> dict:
        if col.parent:
            return {
                "name": col.name,
                "is_visible": col.is_visible,
                "parent": CollectionData.form_collection_dict(col.parent)
            }
        else: 
            return {
                "name": col.name,
                "is_visible": col.is_visible
            }

    def serialize(self) -> dict:
        return self.collections
        
    def deserialize(data: list) -> Self:
        return CollectionData(data)
