import bpy

# Addon Preferences class
class MekAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # Add a toggle property to control the "Development" panel visibility
    enable_development_panel: bpy.props.BoolProperty(
        name="Enable Development Panel",
        description="Show or hide the Development panel in the N-panel",
        default=True
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "enable_development_panel")

        return {'FINISHED'}