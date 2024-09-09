from ..utils.config import data as config
import bpy # type: ignore

# TODO: FIX BUG WHERE FOLDER OPENS FOR DUMP ONLY

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
        op = row.operator(".".join((config["id_name"], "yaml_folder")), text="", icon="FILE_FOLDER")
        op.dev_panel = True

        row = layout.row()
        row.prop(props, "export_yaml_files", text="")
        row.operator(".".join((config["id_name"], "yaml_export")), text="Export YAML", icon="EXPORT")