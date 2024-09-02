import bpy, io, os, yaml # type: ignore
import pathlib
from ..utils.data import BoneData
from ..utils.wrappers import MArmature
from ..utils.config import data as config
from ..utils.tools import get_addon_absolute_path, import_shape_collection
from ..utils.operator_functions import create_and_connect_bones, load_yaml_file, apply_bone_changes, sort_armature_bone_collections


class ARMATURE_OT_CustomShapes(bpy.types.Operator):
    bl_label = "Apply Rig"
    bl_idname = ".".join((config["id_name"], "custom_shapes"))

    def execute(self, context):
        # Check if an Armature is selected
        # Get the armature object
        armature: bpy.types.Object = bpy.context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({"ERROR"},"The active object is not an armature.")
            return {'CANCELLED'}
        
        # Import blend file with custom shapes
        shapes = import_shape_collection(config["custom_shapes_filename"])
        # Get absolute path of yaml file
        filename = context.scene.steps_props.yaml_files
        # filename = ".".join((filename, "yaml"))
        file_path = os.path.join(get_addon_absolute_path(), config["rig_master_files"], filename)
        # Get Variant key
        variant = context.scene.steps_props.variants
        marm = MArmature(armature)

        # Deserialize bone data
        data = load_yaml_file(file_path)
        bones: list[BoneData] = list()
        for obj in data:
            bones.append(BoneData.deserialize(data[obj]))

        create_and_connect_bones(bones, armature, variant)
        apply_bone_changes(bones, marm, armature, variant, shapes)
        sort_armature_bone_collections(bones, armature)
                    
        # Show confirmation Popup
        bpy.ops.wm.show_message('INVOKE_DEFAULT', message="Custom Shapes Applied!")
        return {'FINISHED'}