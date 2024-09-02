from .utils.config import data as config # make sure this loads first to ensure YAML is installed
bl_info = {
    "name": "MekTools",
    "id_name": "mt",
    "author": "G3ru1a",
    "version": (0, 37, 0),
    "blender": (4, 0, 0),
    "location": "View3D > UI > Mektools",
    "description": "Description Goes Here",
    "warning": "warning",
    "doc_url": "url",
    "category": "MekTools 0.37a",
}

import bpy

from .utils.bone_groups import data as bone_groups
from .utils.tools import get_addon_absolute_path, all_operators_in_module

from .panels import armature_controls_panel
from .panels.armature_controls_panel import VisibilityProperties
from .panels.steps_panel import VIEW3D_PT_StepsPanel, StepsProperties
from .panels.dev_panel import VIEW3D_PT_DevPanel, DevProperties
from .panels.links_panel import VIEW3D_PT_LinksPanel
from .panels.inout_panel import VIEW3D_PT_InOutPanel

from .operators import custom_shapes_operator
from .operators import armature_control_operators
from .operators import dev_operators
from .operators import util_operators

# Property to store the last active object
# bpy.types.Scene.last_active_object = bpy.props.PointerProperty(type=bpy.types.Object)

# def armature_selection_handler(scene):
#     current_active_object = bpy.context.view_layer.objects.active
#     if current_active_object != scene.last_active_object:
#         scene.last_active_object = current_active_object
#         if current_active_object and current_active_object.type == 'ARMATURE':
#             on_armature_selected(current_active_object)

# def on_armature_selected(armature):
#     # Your custom code to run when an armature is selected
#     print(f"Selected armature: {armature.name}")

def register_props():
    bpy.utils.register_class(VisibilityProperties)
    bpy.types.Scene.visibility_props = bpy.props.PointerProperty(type=VisibilityProperties)
    bpy.utils.register_class(StepsProperties)
    bpy.types.Scene.steps_props = bpy.props.PointerProperty(type=StepsProperties)
    
    # Visibility Props
    for group in bone_groups:
        prop_name = f"show_{group}".lower().replace(" ", "_")
        # print(prop_name)
        setattr(bpy.types.Scene, prop_name, bpy.props.BoolProperty(
            name=group,
            description=f"Toggle visibility for {group}",
            default=True
        ))

def unregister_props():
    bpy.utils.unregister_class(VisibilityProperties)
    if bpy.types.Scene.visibility_props: del bpy.types.Scene.visibility_props
    bpy.utils.unregister_class(StepsProperties)
    if bpy.types.Scene.steps_props: del bpy.types.Scene.steps_props
    
    # Visibility Props
    for group in bone_groups:
        prop_name = f"show_{group}".lower().replace(" ", "_")
        delattr(bpy.types.Scene, prop_name)

def register():
    register_props()
    # Listener
    # bpy.app.handlers.depsgraph_update_post.append(armature_selection_handler)

    # Development
    if config["production"] is False:
        bpy.utils.register_class(DevProperties)
        bpy.types.Scene.dev_props = bpy.props.PointerProperty(type=DevProperties)
        bpy.utils.register_class(VIEW3D_PT_DevPanel)
        all_operators_in_module(dev_operators, register=True)

    # Dawntrail Functionality

    ## Panels
    bpy.utils.register_class(VIEW3D_PT_LinksPanel)
    bpy.utils.register_class(VIEW3D_PT_InOutPanel)
    bpy.utils.register_class(VIEW3D_PT_StepsPanel)
    bpy.utils.register_class(armature_controls_panel.VIEW3D_PT_ControlsPanel)

    ## Operators
    bpy.utils.register_class(custom_shapes_operator.ARMATURE_OT_CustomShapes)
    all_operators_in_module(armature_control_operators, register=True)
    all_operators_in_module(util_operators, register=True)


def unregister():
    unregister_props()
    # Listener
    # bpy.app.handlers.depsgraph_update_post.remove(armature_selection_handler)
    # del bpy.types.Scene.last_active_object

    # Development
    if config["production"] is False:
        bpy.utils.unregister_class(DevProperties)
        del bpy.types.Scene.dev_props
        bpy.utils.unregister_class(VIEW3D_PT_DevPanel)
        all_operators_in_module(dev_operators, register=False)

    # Dawntrail Functionality

    ## Panels
    bpy.utils.unregister_class(VIEW3D_PT_LinksPanel)
    bpy.utils.unregister_class(VIEW3D_PT_InOutPanel)
    bpy.utils.unregister_class(VIEW3D_PT_StepsPanel)
    bpy.utils.unregister_class(armature_controls_panel.VIEW3D_PT_ControlsPanel)

    ## Operators
    bpy.utils.unregister_class(custom_shapes_operator.ARMATURE_OT_CustomShapes)
    all_operators_in_module(armature_control_operators, register=False)
    all_operators_in_module(util_operators, register=False)

    

if __name__ == "__main__":
    register()
    # bpy.ops.xivrm.armature_select_watcher()    