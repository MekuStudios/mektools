from ..utils.config import data as config
import bpy # type: ignore

class NormalsFix_Mek(bpy.types.Operator):
    bl_label = "Normals Fix"
    bl_idname = ".".join((config["id_name"], "normals_fix"))
    bl_description = "Clear Custom Split Normals if the model looks kinda jank for some reasons."
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        joined_objects = bpy.context.selected_objects
    
        for object in selected_objects:
            if object.type == 'MESH':
                bpy.ops.mesh.customdata_custom_splitnormals_clear() #clear custom split normals
                # Autosmooth is changed in 4.0+ so these two lines don't work right anymore
                # bpy.context.object.data.use_auto_smooth = True  # Set autosmooth to enabled
                # bpy.context.object.data.auto_smooth_angle = radians(180) # Set autosmooth to 180 degrees

        return {'FINISHED'}