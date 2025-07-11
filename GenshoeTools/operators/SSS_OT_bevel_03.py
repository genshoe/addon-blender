import bpy # type: ignore

class SSS_OT_bevel_03(bpy.types.Operator):
	bl_idname = "sss.bevel_03"
	bl_label = "Bevel 0.3mm"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		obj = context.active_object
		if obj.mode != 'EDIT':
			return {'CANCELLED'}
		if obj.type != 'MESH':
			return {'CANCELLED'}
		
		bpy.ops.mesh.bevel(offset=0.0003, offset_pct=0, segments=2, affect='EDGES')
		bpy.ops.mesh.select_less()

		self.report({'INFO'}, "Bevel 0.3mm OK")
		return {'FINISHED'}

def register():
	bpy.utils.register_class(SSS_OT_bevel_03)
def unregister():
	bpy.utils.unregister_class(SSS_OT_bevel_03)
