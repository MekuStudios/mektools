from ..utils.config import data as config
from ..utils.bone_groups import data as bone_groups
import bpy

class VisibilityProperties(bpy.types.PropertyGroup):
    show_unused: bpy.props.BoolProperty(name="Show Unused", default=True) # type: ignore
    show_simple: bpy.props.BoolProperty(name="Show Simple", default=True) # type: ignore
    show_detailed: bpy.props.BoolProperty(name="Show Granular", default=False) # type: ignore
    show_detailed_face: bpy.props.BoolProperty(name="Show Granular Face", default=False) # type: ignore
    show_detailed_head: bpy.props.BoolProperty(name="Show Granular Head", default=False) # type: ignore
    show_detailed_upper_body: bpy.props.BoolProperty(name="Show Granular Upper Body", default=False) # type: ignore
    show_detailed_lower_body: bpy.props.BoolProperty(name="Show Granular Lower Body", default=False) # type: ignore
    show_detailed_equipment: bpy.props.BoolProperty(name="Show Granular Equipment", default=False) # type: ignore
    show_detailed_IVCS: bpy.props.BoolProperty(name="Show Granular IVCS", default=False) # type: ignore

class VIEW3D_PT_ControlsPanel(bpy.types.Panel):
    bl_label = "Rig Layers"
    bl_idname = "VIEW3D_PT_ControlsPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = config["category"]
    
    def draw(self, context):
        layout = self.layout
        props: VisibilityProperties = context.scene.visibility_props

        row = layout.row()
        row.operator(".".join((config["id_name"], "reset_pose")), text="Reset Pose", icon='ARMATURE_DATA')

        # Another section with a header
        layout.label(text="Show/Hide Bones", icon='HIDE_OFF')

        # Create a collapsible box
        box = layout.box()
        row = box.row()
        row.prop(props, "show_unused", icon="TRIA_DOWN" if props.show_unused else "TRIA_RIGHT", icon_only=True, emboss=False)
        row.label(text="Useless(?) Bones")

        if props.show_unused:
            box_row = box.row()
            visibility_operator(context, box_row, "show_noanim", text="NoAnim")
            visibility_operator(context, box_row, "show_prm", text="PRM")
            box_row = box.row()
            visibility_operator(context, box_row, "show_throw", text="n_throw")
            visibility_operator(context, box_row, "show_taillast", text="Tail Extra")

        # Create a collapsible box
        box = layout.box()
        row = box.row()
        row.prop(props, "show_simple", icon="TRIA_DOWN" if props.show_simple else "TRIA_RIGHT", icon_only=True, emboss=False)
        row.label(text="Simple")

        if props.show_simple:
            box_row = box.row()
            visibility_operator(context, box_row, "show_arms")
            visibility_operator(context, box_row, "show_legs")
            box_row = box.row()
            visibility_operator(context, box_row, "show_head")
            box_row = box.row()
            visibility_operator(context, box_row, "show_tail")
            box_row = box.row()
            visibility_operator(context, box_row, "show_gear")
            visibility_operator(context, box_row, "show_equipment")
            box_row = box.row()
            visibility_operator(context, box_row, "show_clothes")
            visibility_operator(context, box_row, "show_twist")

        # Create a collapsible box
        box = layout.box()
        row = box.row()
        row.prop(props, "show_detailed", icon="TRIA_DOWN" if props.show_detailed else "TRIA_RIGHT", icon_only=True, emboss=False)
        row.label(text="Granular")

        if props.show_detailed:

            box_inner = box.box()
            row = box_inner.row()
            row.prop(props, "show_detailed_head", icon="TRIA_DOWN" if props.show_detailed_head else "TRIA_RIGHT", icon_only=True, emboss=False)
            row.label(text="Head")

            if props.show_detailed_head:
        
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_neck")
                visibility_operator(context, box_row, "show_headcore", text="Head Tilt")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_hair")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_ears")
                visibility_operator(context, box_row, "show_earrings")

            box_inner = box.box()
            row = box_inner.row()
            row.prop(props, "show_detailed_face", icon="TRIA_DOWN" if props.show_detailed_face else "TRIA_RIGHT", icon_only=True, emboss=False)
            row.label(text="Face")

            if props.show_detailed_face:
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_jaw")
                visibility_operator(context, box_row, "show_nose")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_mouth")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_eyebrows")
                visibility_operator(context, box_row, "show_eyelids")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_cheeks")
                visibility_operator(context, box_row, "show_pupils")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_facedrag")
            
            box_inner = box.box()
            row = box_inner.row()
            row.prop(props, "show_detailed_upper_body", icon="TRIA_DOWN" if props.show_detailed_upper_body else "TRIA_RIGHT", icon_only=True, emboss=False)
            row.label(text="Upper Body")

            if props.show_detailed_upper_body:
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_handleft")
                visibility_operator(context, box_row, "show_handright")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_twist")
                visibility_operator(context, box_row, "show_armsfk", text="Arms FK")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_spine")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_clavicles")
                visibility_operator(context, box_row, "show_boobs")
            
            row = box.row()
            visibility_operator(context, row, "show_waist")

            box_inner = box.box()
            row = box_inner.row()
            row.prop(props, "show_detailed_lower_body", icon="TRIA_DOWN" if props.show_detailed_lower_body else "TRIA_RIGHT", icon_only=True, emboss=False)
            row.label(text="Lower Body")

            if props.show_detailed_lower_body:
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_toes")
                visibility_operator(context, box_row, "show_ankles")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_hips")
                visibility_operator(context, box_row, "show_tail")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_legfk", text="Legs FK")
            
            box_inner = box.box()
            row = box_inner.row()
            row.prop(props, "show_detailed_equipment", icon="TRIA_DOWN" if props.show_detailed_equipment else "TRIA_RIGHT", icon_only=True, emboss=False)
            row.label(text="Equipment")

            if props.show_detailed_equipment:
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_clothes")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_kneegear", text="Knee Gear")
                visibility_operator(context, box_row, "show_elbowgear", text="Elbow Gear")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_shouldergear", text="Shoulder Gear")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_shields", text="Shields")
                visibility_operator(context, box_row, "show_weaponhand", text="Weapon Hand")
                box_row = box_inner.row()
                visibility_operator(context, box_row, "show_weaponwaist", text="Weapon Waist")
                visibility_operator(context, box_row, "show_weaponback", text="Weapon Back")
            
            box_inner = box.box()
            row = box_inner.row()
            row.prop(props, "show_detailed_IVCS", icon="TRIA_DOWN" if props.show_detailed_IVCS else "TRIA_RIGHT", icon_only=True, emboss=False)
            row.label(text="IVCS")

            if props.show_detailed_IVCS:
                box_row = box_inner.row()
                box_row.label(text="To Be Added...")



def visibility_operator(context, box, prop: str, text: str = None):
    depress = getattr(context.scene, prop);
    if text is None: text = prop.split("_")[1].capitalize()
    op = box.operator(".".join((config["id_name"], "toggle_visibility")), text=text,
                    depress=depress)
    op.bone_group_key = prop.split("_")[1]
    op.visibility_prop = prop
    
