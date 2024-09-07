from typing import Tuple, List
import bpy
import mathutils
from mathutils import Vector
from ..tools import mode_set
from .bones import MPoseBone, MEditBone, MBone
from mathutils import kdtree
from mathutils.kdtree import KDTree
from ..bone_groups import reference_bones
from ..tools import is_bone_created
import math


class MArmature:
    armature: bpy.types.Object = None
    data: bpy.types.Armature = None
    kdtree_head: KDTree = None
    kdtree_tail: KDTree = None

    def __init__(self, armature: bpy.types.Object) -> None:
        self.armature = armature
        self.data = armature.data

    def add_bone_to_collection(self, bone: bpy.types.Bone, collection_name: str) -> None:
        # Create the collection if it doesn't exist, then add the bone to it
        if collection_name not in self.data.collections:
            self.data.collections.new(collection_name)
        with mode_set(mode="POSE"):
            self.data.collections[collection_name].assign(bone)

    def pose_bone(self, bone_name: str) -> MPoseBone:
        with mode_set(mode="POSE"):
            if bone_name is None: return;
            bone = self.armature.pose.bones.get(bone_name)
            if bone is None:
                return None
            return MPoseBone(bone);

    def bone(self, bone_name: str) -> bpy.types.Bone:
        if bone_name is None: return;
        if bone_name in self.data.bones:
            return self.data.bones[bone_name]
        else:
            return None

    def edit_bone(self, bone_name: str) -> MEditBone:
        if bone_name is None: return;
        bone = self.data.edit_bones.get(bone_name)
        if bone is None:
            return None
        return MEditBone(bone);

    def build_kdtrees(self):
        size = len(self.data.bones)  # Number of bones
        kd_tree = kdtree.KDTree(size)

        with mode_set(mode="EDIT"):
            for i, bone in enumerate(self.data.edit_bones):
                # Ignore if the bone is not vanilla
                if bone.name not in reference_bones: continue
                kd_tree.insert(bone.head, i)  # Insert bone head position and index

        kd_tree.balance()  # Balance the tree for faster queries
        self.kdtree_head = kd_tree
        kd_tree = kdtree.KDTree(size)

        with mode_set(mode="EDIT"):
            for i, bone in enumerate(self.data.edit_bones):
                # Ignore if the bone is not a reference bone
                if bone.name not in reference_bones: continue
                kd_tree.insert(bone.tail, i)  # Insert bone tail position and index

        kd_tree.balance()  # Balance the tree for faster queries
        self.kdtree_tail = kd_tree
    
    def nearest_bone_dict(self, bone_position, bone_name) -> dict:
        nearest_head = self.nearest_bone(self.kdtree_head, bone_position, bone_name)
        nearest_tail = self.nearest_bone(self.kdtree_tail, bone_position, bone_name)

        head_dist = math.dist(bone_position, nearest_head.head)
        tail_dist = math.dist(bone_position, nearest_tail.tail)

        if tail_dist < head_dist:
            return {"bone": nearest_tail, "head": False}
        else:
            return {"bone": nearest_head, "head": True}
        
    
    def nearest_bone_tail(self, bone: bpy.types.EditBone) -> bpy.types.EditBone:
        return self.nearest_bone(self.kdtree_tail, bone.tail, bone.name)

    def nearest_bone(self, kdtree: KDTree, bone_pos: List[float] | Tuple[float, float, float] | Vector, bone_name: str):
        if not kdtree:
            raise ValueError("KDTree has not been built but an access attempt has been made.")
        with mode_set(mode="EDIT"):
            # Find the nearest point (bone head) to the reference bone head
            location, index, distance = kdtree.find(bone_pos)

            # Use the index to get the nearest bone
            nearest_bone = self.data.edit_bones[index]
            if nearest_bone.name == bone_name:
                # If the nearest bone is the reference bone itself, find the second nearest
                location, index, distance = kdtree.find_n(bone_pos, 2)[-1]
                nearest_bone = self.data.edit_bones[index]

            return nearest_bone