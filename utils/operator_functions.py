import io, os, yaml # type: ignore
import pathlib
import bpy

from .tools import mode_set

from .wrappers.armature import MArmature
from .wrappers.bones import MPoseBone
from .data import BoneData


def load_yaml_file(filepath: str) -> any:
    # Mak sure the file exists
    my_file = pathlib.Path(filepath)
    if not my_file.is_file():
        bpy.ops.wm.show_message('INVOKE_DEFAULT', message="Could not find YAML file.")
        return {'CANCELLED'}

    # Load the file data
    with io.open(filepath, 'r') as stream:
        data = yaml.safe_load(stream)
    
    return data

def create_and_connect_bones(bones: list[BoneData], armature: object, variant: str):
    with mode_set(mode="EDIT"):
        # Create Missing Bones
        for bone_data in bones: 
            if not bone_data.should_create: 
                continue
            # Update Existing Bones
            existing_bones = {bone.name: bone for bone in armature.data.edit_bones}
            
            v = bone_data.get_variant(variant_name=variant)
            v.edit_data.create(armature, bone_data.name, existing_bones)

        # Update Existing Bones
        existing_bones = {bone.name: bone for bone in armature.data.edit_bones}
        # Connect Added Bones
        for bone_data in bones: 
            if not bone_data.should_create: 
                continue
            
            v = bone_data.get_variant(variant_name=variant)
            v.edit_data.connect(armature, bone_data.name, existing_bones)

def apply_bone_changes(bones: list[BoneData], marm: MArmature, armature: object, variant: str, shapes: dict):
    # Apply Changes
    for bone_data in bones:
        # Get Variant Data
        v = bone_data.get_variant(variant_name=variant)
        csd = v.custom_shape_data
        
        # Get Bone
        bone: bpy.types.Bone = marm.bone(bone_name=bone_data.name)
        pbone: MPoseBone = marm.pose_bone(bone_name=bone_data.name)

        # Setup Bone's Collections
        if bone_data.bone_collections:
            #armature.data because blender api is cringe, same as MArmature
            bone_data.bone_collections.create_and_attach(armature.data, bone)

        # Apply Custom Shape
        if pbone and csd and csd.shape_name: 
            pbone.set_custom_shape(custom_shape_object=shapes.get(csd.shape_name), 
                                custom_shape_data=csd)
        # Apply Visibility
        if pbone: 
            pbone.set_visibility(bone_data.visible)

        # Apply Constraints
        if pbone and v and v.constraint_data:
            # Remove all constraints from the bone to avoid duplication
            for constraint in pbone.bone.constraints:
                pbone.bone.constraints.remove(constraint)
            # Create Variant Constraints
            for cd in v.constraint_data:
                cd.create(pbone.bone, armature)

def sort_armature_bone_collections(bones: list[BoneData], armature: object):
    for bone_data in bones:
        bone_data.bone_collections.sort_collections(armature=armature.data)


