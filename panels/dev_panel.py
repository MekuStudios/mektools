from ..utils.config import data as config
from ..utils import yaml_files
import bpy

def yaml_files_enum_callback(self, context):
    return yaml_files.get_editable_files()

def variants_enum_callback(self, context):
    return config["variants"]

class DevProperties(bpy.types.PropertyGroup):
    dump_file_name: bpy.props.StringProperty(name="Text Field", default="custom_shapes") # type: ignore
    variants: bpy.props.EnumProperty(
        name="Variants Enum",
        description="Choose A Variant",
        items=variants_enum_callback
    ) # type: ignore
    yaml_files: bpy.props.EnumProperty(
        name="No YAML files found.",
        description="Choose A YAML File",
        items=yaml_files_enum_callback
    ) # type: ignore
    preview_yaml_files: bpy.props.EnumProperty(
        name="No YAML files found.",
        description="Choose A YAML File",
        items=yaml_files_enum_callback
    ) # type: ignore
    preview_variants: bpy.props.EnumProperty(
        name="Variants Enum",
        description="Choose A Variant",
        items=variants_enum_callback
    ) # type: ignore
    export_yaml_files: bpy.props.EnumProperty(
        name="Select a YAML File",
        description="Choose A YAML File",
        items=yaml_files_enum_callback
    ) # type: ignore

class VIEW3D_PT_DevPanel(bpy.types.Panel):
    bl_label = "Development"
    bl_idname = "VIEW3D_PT_DevPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = config["category"]

    def poll(cls, context):
        # Access addon preferences to check if the panel should be shown
        prefs = bpy.context.preferences.addons[__name__].preferences
        return prefs.enable_development_panel
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.dev_props

        # TODO: Add a way to export/import the rigfile-- ((wait you did this already right? -))
        layout.label(text="Import / Export", icon='TEMP')
        row = layout.row()
        op = row.operator(".".join((config["id_name"], "yaml_import")), text="Import YAML", icon="IMPORT")
        op.dev_panel = True
        op = row.operator(".".join((config["id_name"], "yaml_folder")), text="", icon="FILE_FOLDER")
        op.dev_panel = True

        row = layout.row()
        row.prop(props, "export_yaml_files", text="")
        op = row.operator(".".join((config["id_name"], "yaml_export")), text="Export YAML", icon="EXPORT")
        op.dev_panel = True

        # Another section with a header
        layout.separator()  # Adds visual separation between sections
        layout.label(text="New Configuration", icon='FILE_NEW')

        layout.prop(props, "dump_file_name", text="Filename")
        
        row = layout.row()
        row.operator(".".join((config["id_name"], "export_to_yaml")), text="Generate YAML")

        # Another section with a header
        layout.separator()  # Adds visual separation between sections
        layout.label(text="Edit Variants", icon='MODIFIER')

        row = layout.row()
        row.alignment = 'CENTER'
        # row.label(text="Select a YAML File")
        layout.prop(props, "yaml_files", text="YAML")

        row = layout.row()
        row.alignment = 'CENTER'
        # row.label(text="Select a Variant")
        layout.prop(props, "variants", text="Variant")

        row = layout.row()
        row.operator(".".join((config["id_name"], "append_variant_to_yaml")), text="Update Variant")

        # Another section with a header
        layout.separator()  # Adds visual separation between sections
        layout.label(text="Preview YAML Configuration", icon='VIEWZOOM')
        
        
        row = layout.row()
        layout.prop(props, "preview_yaml_files", text="YAML")

        row = layout.row()
        layout.prop(props, "preview_variants", text="Variant")
        row = layout.row()
        row.operator(".".join((config["id_name"], "apply_from_yaml")), text="Apply")
    

