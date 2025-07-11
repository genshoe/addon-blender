import bpy

class SSS_OT_subdivision_toggle(bpy.types.Operator):
	bl_idname = "sss.subdivision_toggle"
	bl_label = "Subdivision toggle"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		selected = context.selected_objects
		if len(selected)>0:
			if bpy.ops.object.mode_set.poll():
				bpy.ops.object.mode_set(mode="OBJECT")	
			for x in selected:
				if x.type=="MESH" and x.modifiers.get("Subdivision"):
					if x.modifiers["Subdivision"].show_render == True:
						x.modifiers["Subdivision"].show_on_cage = False
						x.modifiers["Subdivision"].show_in_editmode = False
						x.modifiers["Subdivision"].show_viewport = False
						x.modifiers["Subdivision"].show_render = False
						
					elif x.modifiers["Subdivision"].show_render == False:
						x.modifiers["Subdivision"].show_on_cage = True
						x.modifiers["Subdivision"].show_in_editmode = True
						x.modifiers["Subdivision"].show_viewport = True
						x.modifiers["Subdivision"].show_render = True

		return {'FINISHED'}
	
def register():
	bpy.utils.register_class(SSS_OT_subdivision_toggle)
def unregister():
	bpy.utils.unregister_class(SSS_OT_subdivision_toggle)