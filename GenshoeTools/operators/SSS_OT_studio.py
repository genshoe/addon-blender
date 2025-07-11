import bpy

def register():
	bpy.utils.register_class(SSS_OT_studio)
def unregister():
	bpy.utils.unregister_class(SSS_OT_studio)

class SSS_OT_studio(bpy.types.Operator):
	bl_idname = "sss.studio"
	bl_label = "Setup studio"
	bl_options = {'REGISTER', 'UNDO'}

#	@classmethod
#	def poll(cls, context):
#		if bpy.context.area.ui_type != 'UV':
#			return False
#		if not bpy.context.active_object:
#			return False
#		if bpy.context.active_object.mode != 'EDIT':
#			return False
#		if bpy.context.active_object.type != 'MESH':
#			return False
#		if not bpy.context.object.data.uv_layers:
#			return False
#		if bpy.context.scene.tool_settings.use_uv_select_sync:
#			return False
#		return True
	
	def execute(self, context):
		main(self, context)
		self.report({'INFO'}, "OK")
		return {'FINISHED'}
	
def main(self, context):
	self.report({'INFO'}, "OK test")