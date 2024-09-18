from ..utils.config import data as config
import bpy # type: ignore

class MATERIAL_OT_AlphaFix(bpy.types.Operator):
    bl_label = "Alpha Fix"
    bl_idname = ".".join((config["id_name"], "alpha_fix"))

    def execute(self, context):
        for item in bpy.data.materials:
            item.blend_method = 'HASHED' # Such a smol function, much wow
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)