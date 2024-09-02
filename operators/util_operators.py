import bpy, yaml # type: ignore
from ..utils.config import data as config



#TODO: Finish this import Export logic

class ExportYAML(bpy.types.Operator):
    """Export to YAML"""
    bl_idname = ".".join((config["id_name"], "yaml_export"))
    bl_label = "Export YAML"
    bl_options = {'REGISTER'}

    # Define properties
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore

    # This method is called when the operator is executed to invoke a file selector
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        # Use the selected file path to save the YAML file
        data = {'example': 'data'}  # Replace with your actual data logic
        if not self.filepath.endswith('.yaml'):
            self.filepath += '.yaml'
        with open(self.filepath, 'w') as file:
            yaml.dump(data, file)
        return {'FINISHED'}

class ImportYAML(bpy.types.Operator):
    """Import from YAML"""
    bl_idname = ".".join((config["id_name"], "yaml_import"))
    bl_label = "Import YAML"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        # Use the selected file path to load the YAML file
        with open(self.filepath, 'r') as file:
            data = yaml.safe_load(file)
        print(data)  # Replace with your actual processing logic
        return {'FINISHED'}