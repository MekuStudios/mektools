from ..utils.config import data as config
import bpy # type: ignore


class VIEW3D_IMPORT_AND_EXPORT_FBX(bpy.types.Panel):
    bl_label = "Import and Export"
    bl_idname = 'VIEW3D_IMPORT_AND_EXPORT_FBX'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = config["category"]

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        # Box and Split section for the import/export buttons
        inout_box = layout.box()
        inout_split = inout_box.split(factor=0.5, align=False)
        
        # Buttons for Import and export FBX
        op = inout_split.operator('import_scene.fbx', text='Import FBX', icon_value=706, emboss=True, depress=False)        
        op = inout_split.operator('export_scene.fbx', text='Export FBX', icon_value=707, emboss=True, depress=False)
        
        # Box and split for the object fix buttons
        fix_box = layout.box()
        fix_split = fix_box.split(factor=0.5, align=False)
        
        # Buttons for Clear Parents, Fix Alpha, Fix Normals.
        op = fix_split.operator('object.parent_clear', text='Clear Parents', icon_value=0, emboss=True, depress=False)
        op.type = 'CLEAR_KEEP_TRANSFORM'
        
        op = fix_split.operator(".".join((config["id_name"], "alpha_fix")), text="Fix Alpha", icon_value=0, emboss=True, depress=False)

        op = fix_box.operator(".".join((config["id_name"], "normals_fix")), text="Fix Normals", icon_value=0, emboss=True, depress=False)