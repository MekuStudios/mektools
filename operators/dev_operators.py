import bpy, io, os, yaml # type: ignore
import string, random, pathlib

from ..utils.data import BoneData, CustomShapeData, Variant
from ..utils.config import data as config
from ..utils.tools import mode_set, get_addon_absolute_path, import_shape_collection, lists_are_equal
from ..utils.armature import RM_Armature

class MyDumper(yaml.SafeDumper):
    pass

def represent_list(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

MyDumper.add_representer(list, represent_list)

class WM_OT_ShowMessage(bpy.types.Operator):
    bl_idname = "wm.show_message"
    bl_label = "Action Executed"

    message: bpy.props.StringProperty(name="Message", default="Action completed successfully!") # type: ignore

    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message)

class ARMATURE_OT_ExportBonesToYAML(bpy.types.Operator):
    """Export current armature shapes to YAML File"""
    bl_label = "Export To YAML"
    bl_idname = ".".join((config["id_name"], "export_to_yaml"))
    
    def execute(self, context):
         # Check if an Armature is selected
        # Get the armature object
        armature: bpy.types.Object = bpy.context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({"ERROR"},"The active object is not an armature.")
            return {'CANCELLED'}
        
        variant = "default"

        # Loop through all the bones and write changes of only bones that have a custom shape attached
        data = {};
        with mode_set(mode="POSE"):
            for bone in armature.pose.bones:
                if bone.custom_shape: #TEMPORARY
                    bone_data: BoneData = BoneData.from_bone(bone)
                    bone_name = str(bone.name)
                    
                    if bone.custom_shape:
                        csd = CustomShapeData.from_bone(bone)
                        variant_data = Variant(csd)
                        bone_data.add_variant(variant=variant_data, variant_name=variant)

                    data[bone_name] = bone_data.serialize()
                
        
        # Compute absolute path
        filename = context.scene.dev_props.dump_file_name
        filename = ".".join((filename, "yaml"))
        dump_file_path = os.path.join(get_addon_absolute_path(), config["yaml_files_folder"], filename)

        # Delete the file if it exists
        my_file = pathlib.Path(dump_file_path)
        if my_file.is_file():
            my_file.unlink()

        # Write new file 
        with io.open(dump_file_path, 'x') as outfile:
            yaml.dump(data, outfile, Dumper=MyDumper, default_flow_style=False, allow_unicode=True)
        
        # Show confirmation Popup
        bpy.ops.wm.show_message('INVOKE_DEFAULT', message="YAML File generated successfully!")
        return {'FINISHED'}
    
class ARMATURE_OT_ApplyYAMLCustomShapes(bpy.types.Operator):
    """Apply sesttings from YAML File"""
    bl_label = "Apply from YAML"
    bl_idname = ".".join((config["id_name"], "apply_from_yaml"))

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
        filename = context.scene.dev_props.preview_yaml_files
        # filename = ".".join((filename, "yaml"))
        file_path = os.path.join(get_addon_absolute_path(), config["yaml_files_folder"], filename)

        # Get Variant key
        variant = context.scene.dev_props.preview_variants

        # Mak sure the file exists
        my_file = pathlib.Path(file_path)
        if not my_file.is_file():
            bpy.ops.wm.show_message('INVOKE_DEFAULT', message="Could not find YAML file.")
            return {'CANCELLED'}

        # Load the file data
        with io.open(file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Deserialize bone data
        bones: list[BoneData] = list()
        for obj in data:
            bones.append(BoneData.deserialize(data[obj]))

        # Apply changes
        rma = RM_Armature(armature=armature)
        for bone_data in bones:
            v = bone_data.get_variant(variant_name=variant)
            csd = v.custom_shape_data;
            bone = rma.get_bone(bone_data.name)
            if bone is None: continue
            bone.set_custom_shape(shapes.get(csd.shape_name), scale=csd.scale)
            bone.set_custom_shape_offset(csd.offset)
            bone.set_custom_shape_rotation_euler(csd.rotation)
            bone.set_custom_shape_color(csd.shape_color)
        
        # Show confirmation Popup
        bpy.ops.wm.show_message('INVOKE_DEFAULT', message="Custom Shapes Applied!")
        return {'FINISHED'}
    
class ARMATURE_OT_AppendVariantToYAML(bpy.types.Operator):
    """Append current differences as Variant to YAML File"""
    bl_label = "Export To YAML"
    bl_idname = ".".join((config["id_name"], "append_variant_to_yaml"))
    
    def execute(self, context):
         # Check if an Armature is selected
        # Get the armature object
        armature: bpy.types.Object = bpy.context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({"ERROR"},"The active object is not an armature.")
            return {'CANCELLED'}
        
        # Compute absolute path for the YAML file
        filename = context.scene.dev_props.yaml_files
        # filename = ".".join((filename, "yaml"))
        dump_file_path = os.path.join(get_addon_absolute_path(), config["yaml_files_folder"], filename)

        # Makse sure the file exists
        my_file = pathlib.Path(dump_file_path)
        if not my_file.is_file():
            bpy.ops.wm.show_message('INVOKE_DEFAULT', message="Could not find YAML file.")
            return {'CANCELLED'}

        # Load the file data
        with io.open(dump_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Deserialize bone data
        bones: dict[BoneData] = {}
        for obj in data:
            bone_data: BoneData = BoneData.deserialize(data[obj])
            bones[bone_data.name] = bone_data

        # Get Variant key
        variant = context.scene.dev_props.variants

        # Go through each bone and add or overrwide the saved bone data.
        with mode_set(mode="POSE"):
            for bone in armature.pose.bones:
                if bone.custom_shape: #TEMPORARY
                    bone_name = str(bone.name)
                    bone_data: BoneData = bones[bone_name]
                    
                    if bone.custom_shape:
                        csd = CustomShapeData.from_bone(bone)
                        variant_data = Variant(csd)
                        bone_data.add_variant(variant=variant_data, variant_name=variant,
                                              overwrite=True)

                    bones[bone_name] = bone_data
        
        # Serialize the new data
        data = {}
        for bone_name, bone_data in bones.items():
            data[bone_name] = bone_data.serialize()

        # Delete YAML file
        my_file.unlink()

        # Write new data
        with io.open(dump_file_path, 'x') as outfile:
            yaml.dump(data, outfile, Dumper=MyDumper, default_flow_style=False, allow_unicode=True)
        bpy.ops.wm.show_message('INVOKE_DEFAULT', message="Updated YAML File!")
        return {'FINISHED'}

