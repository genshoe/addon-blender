import bpy

class SSS_OT_shrink_03(bpy.types.Operator):
	bl_idname = "sss.shrink_03"
	bl_label = "Shrink -0.3mm"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = context.active_object
		if obj.mode != 'EDIT' or obj.type != 'MESH':
			return {'CANCELLED'}
		
		bpy.ops.transform.shrink_fatten(value=-0.0003)

		self.report({'INFO'}, "Shrink -0.3mm OK")
		return {'FINISHED'}
	
def register():
	bpy.utils.register_class(SSS_OT_shrink_03)
def unregister():
	bpy.utils.unregister_class(SSS_OT_shrink_03)
