import bpy
import mathutils
from ..tools import mode_set
from .bones import MPoseBone, MEditBone, MBone

class MArmature:
    armature: bpy.types.Object = None
    data: bpy.types.Armature = None

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
        bone = self.data.bones[bone_name]
        if bone is None:
            return None
        return bone

    def edit_bone(self, bone_name: str) -> MEditBone:
        if bone_name is None: return;
        bone = self.data.edit_bones.get(bone_name)
        if bone is None:
            return None
        return MEditBone(bone);