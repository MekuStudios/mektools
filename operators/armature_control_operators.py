import bpy
from ..utils.config import data as config
from ..utils.bone_groups import data as bone_groups
from ..utils.tools import mode_set
from ..utils.armature import RM_Armature

class ARMATURE_OT_ToggleVisibility(bpy.types.Operator):
    """Base class for toggling visibility of armature components"""
    bl_label = "Toggle Visibility"
    bl_idname = ".".join((config["id_name"], "toggle_visibility"))

    bone_group_key: bpy.props.StringProperty(default="arms") # type: ignore
    visibility_prop: bpy.props.StringProperty(default="show_arms") # type: ignore
    
    def execute(self, context):
         # Check if an Armature is selected
        # Get the armature object
        armature: bpy.types.Object = bpy.context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({"ERROR"},"The active object is not an armature.")
            return {'CANCELLED'}
        # shapes = import_shape_collection(config.custom_shapes_filename)
        rm_armature = RM_Armature(armature=armature)
        visible: bool = False
        
        # print(bone_groups[self.bone_group_key])
        # print(self.visibility_prop)
        for bone in bone_groups[self.bone_group_key]:
            bone = rm_armature.get_bone(bone);
            if bone is None: continue
            visible = bone.toggle_visibility()
        
        setattr(context.scene, self.visibility_prop, visible)
        return {'FINISHED'}

class ARMATURE_OT_PoseReset(bpy.types.Operator):
    bl_label = "Reset Pose"
    bl_idname = ".".join((config["id_name"], "reset_pose"))
    
    def execute(self, context):
        # Check if an Armature is selected
        # Get the armature object
        armature: bpy.types.Object = bpy.context.active_object
        if not armature or armature.type != 'ARMATURE':
            print("The active object is not an armature.")
            return

        # Reset Bone Positions and Rotations
        with mode_set(mode="POSE"):
            for bone in armature.pose.bones:
                # Clear transformations
                bone.location = (0, 0, 0)      # Reset translation
                bone.rotation_quaternion = (1, 0, 0, 0)  # Reset quaternion rotation
                bone.rotation_euler = (0, 0, 0)  # Reset Euler rotation (will only work for objects using this mode)

        # Make sure Armature is showed in front
        armature.show_in_front = True
        return {'FINISHED'}