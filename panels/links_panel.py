from ..utils.config import data as config
import bpy

class VIEW3D_PT_LinksPanel(bpy.types.Panel):
    bl_label = config["category"]
    bl_idname = 'VIEW3D_PT_LinksPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = config["category"]

    def draw(self, context):
        layout = self.layout
        exec('op =' + 'layout.' + 'operator(' + "'wm.url_open'," + "text='Support me on Patreon!'," + 'icon_value=227,' + 'emboss=True,' + 'depress=False,)' + ".url = '" + 'https://www.patreon.com/MekuuMaki' + "'")
        exec('op =' + 'layout.' + 'operator(' + "'wm.url_open'," + "text='Join the Discord! (18+ only)'," + 'icon_value=227,' + 'emboss=True,' + 'depress=False,)' + ".url = '" + 'https://www.discord.gg/98DqcKE' + "'")