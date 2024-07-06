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
        #