from ..utils.config import data as config
import bpy # type: ignore


class VIEW3D_IMPORT_AND_EXPORT_MEK(bpy.types.Panel):
    bl_label = "Import and Export"
    bl_idname = 'VIEW3D_IMPORT_AND_EXPORT_MEK'
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
        box_1056A = layout.box()
        box_1056A.alert = False
        box_1056A.enabled = True
        box_1056A.active = True
        box_1056A.use_property_split = False
        box_1056A.use_property_decorate = False
        box_1056A.alignment = 'Expand'.upper()
        box_1056A.scale_x = 1.0
        box_1056A.scale_y = 1.0
        if not True: box_1056A.operator_context = "EXEC_DEFAULT"
        split_57605 = box_1056A.split(factor=0.5, align=False)
        split_57605.alert = False
        split_57605.enabled = True
        split_57605.active = True
        split_57605.use_property_split = False
        split_57605.use_property_decorate = False
        split_57605.scale_x = 1.0
        split_57605.scale_y = 1.0
        split_57605.alignment = 'Expand'.upper()
        if not True: split_57605.operator_context = "EXEC_DEFAULT"
        
        # Buttons for Import and export FBX
        # These don't need a special config thing because they are blender default operators.
        op = split_57605.operator('import_scene.fbx', text='Import FBX', icon_value=706, emboss=True, depress=False)        
        op = split_57605.operator('export_scene.fbx', text='Export FBX', icon_value=707, emboss=True, depress=False)
        
        
        box_FEE47 = layout.box()
        box_FEE47.alert = False
        box_FEE47.enabled = True
        box_FEE47.active = True
        box_FEE47.use_property_split = False
        box_FEE47.use_property_decorate = False
        box_FEE47.alignment = 'Expand'.upper()
        box_FEE47.scale_x = 1.0
        box_FEE47.scale_y = 1.0
        if not True: box_FEE47.operator_context = "EXEC_DEFAULT"
        split_7EDD2 = box_FEE47.split(factor=0.5, align=False)
        split_7EDD2.alert = False
        split_7EDD2.enabled = True
        split_7EDD2.active = True
        split_7EDD2.use_property_split = False
        split_7EDD2.use_property_decorate = False
        split_7EDD2.scale_x = 1.0
        split_7EDD2.scale_y = 1.0
        split_7EDD2.alignment = 'Expand'.upper()
        if not True: split_7EDD2.operator_context = "EXEC_DEFAULT"
        
        # Buttons for Clear Parents, Fix Alpha, Fix Normals.
        # Clear parents don't need a special config thing because they are blender default operators.

        op = split_7EDD2.operator('object.parent_clear', text='Clear Parents', icon_value=0, emboss=True, depress=False)
        op.type = 'CLEAR_KEEP_TRANSFORM'
        
        op = split_7EDD2.operator(".".join((config["id_name"], "alpha_fix")), text="Fix Alpha", icon_value=0, emboss=True, depress=False)

        op = box_FEE47.operator(".".join((config["id_name"], "normals_fix")), text="Fix Normals", icon_value=0, emboss=True, depress=False)