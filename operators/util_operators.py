import bpy, yaml # type: ignore
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..utils.config import data as config
from ..utils.tools import get_addon_absolute_path
import os
import shutil


#TODO: Finish this import Export logic

class ExportYAML(bpy.types.Operator, ExportHelper):
    """Export to YAML"""
    bl_idname = ".".join((config["id_name"], "yaml_export"))
    bl_label = "Export YAML"
    bl_options = {'REGISTER'}

    dev_panel: bpy.props.BoolProperty(default=False) # type: ignore

    # ExportHelper mix-in class uses this.
    filename_ext = ".yaml"

    filter_glob:  bpy.props.StringProperty(
        default="*.yaml",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )# type: ignore

    def execute(self, context):
        # Use the selected file path to save the YAML file
        if not self.filepath.endswith('.yaml'):
            self.filepath += '.yaml'

        # Get absolute path of yaml file
        if self.dev_panel:
            yaml_filename = context.scene.dev_props.export_yaml_files
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["yaml_files_folder"], yaml_filename)
        else:
            yaml_filename = context.scene.steps_props.export_yaml_files
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["rig_master_files"], yaml_filename)

        shutil.copy2(yaml_file_path, self.filepath)
        return {'FINISHED'}

class ImportYAML(bpy.types.Operator, ImportHelper):
    """Import from YAML"""
    bl_idname = ".".join((config["id_name"], "yaml_import"))
    bl_label = "Import YAML"

    dev_panel: bpy.props.BoolProperty(default=False, options={'HIDDEN'}) # type: ignore

    # ExportHelper mix-in class uses this.
    filename_ext = ".yaml"

    filter_glob:  bpy.props.StringProperty(
        default="*.yaml",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )# type: ignore

    def execute(self, context):
        # Use the selected file path to save the YAML file
        if not self.filepath.endswith('.yaml'):
            self.filepath += '.yaml'

        # Get absolute path of yaml file
        if self.dev_panel:
            yaml_filename = os.path.basename(self.filepath)
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["yaml_files_folder"], yaml_filename)
        else:
            yaml_filename = os.path.basename(self.filepath)
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["rig_master_files"], yaml_filename)

        shutil.copy2(self.filepath, yaml_file_path)
        return {'FINISHED'}
    
class ExportYAML(bpy.types.Operator, ExportHelper):
    """Export to YAML"""
    bl_idname = ".".join((config["id_name"], "yaml_export"))
    bl_label = "Export YAML"
    bl_options = {'REGISTER'}

    dev_panel: bpy.props.BoolProperty(default=False) # type: ignore

    # ExportHelper mix-in class uses this.
    filename_ext = ".yaml"

    filter_glob:  bpy.props.StringProperty(
        default="*.yaml",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )# type: ignore

    def execute(self, context):
        # Use the selected file path to save the YAML file
        if not self.filepath.endswith('.yaml'):
            self.filepath += '.yaml'

        # Get absolute path of yaml file
        if self.dev_panel:
            yaml_filename = context.scene.dev_props.export_yaml_files
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["yaml_files_folder"], yaml_filename)
        else:
            yaml_filename = context.scene.steps_props.export_yaml_files
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["rig_master_files"], yaml_filename)

        shutil.copy2(yaml_file_path, self.filepath)
        return {'FINISHED'}

class OpenYAMLFolder(bpy.types.Operator):
    """Import from YAML"""
    bl_idname = ".".join((config["id_name"], "yaml_folder"))
    bl_label = "Open YAML Folder"

    dev_panel: bpy.props.BoolProperty(default=False, options={'HIDDEN'}) # type: ignore

    def execute(self, context):

        # Get absolute path of yaml file
        if self.dev_panel:
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["yaml_files_folder"])
        else:
            yaml_file_path = os.path.join(get_addon_absolute_path(), config["rig_master_files"])

        os.startfile(yaml_file_path)
        return {'FINISHED'}