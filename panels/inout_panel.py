from ..utils.config import data as config
import bpy

class VIEW3D_PT_InOutPanel(bpy.types.Panel):
    bl_label = "Import / Export"
    bl_idname = 'VIEW3D_PT_InOutPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = config["category"]

    def draw(self, context):
        layout = self.layout
        props = context.scene.steps_props
        
        layout.label(text="Import / Export", icon='TEMP')
        row = layout.row()
        row.operator(".".join((config["id_name"], "yaml_import")), text="Import YAML", icon="IMPORT")
        
        row = layout.row()
        row.prop(props, "yaml_files", text="")
        row.operator(".".join((config["id_name"], "yaml_export")), text="Export YAML", icon="EXPORT")