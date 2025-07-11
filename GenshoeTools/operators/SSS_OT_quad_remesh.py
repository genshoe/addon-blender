import bpy

class SSS_OT_quad_remesh(bpy.types.Operator):
	bl_idname = "sss.quad_remesh"
	bl_label = "Quad Remesh"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		# Đảm bảo đang ở chế độ Object Mode
		bpy.ops.object.mode_set(mode='OBJECT')
		obj = context.active_object
		if not obj or obj.type!= 'CURVE':
			self.report({'WARNING'}, "Curve")
			return {'CANCELLED'}

		# Duplicate curve
		#bpy.ops.object.duplicate(linked=False)

		# Curve to mesh
		bpy.ops.object.convert(target='MESH')

		# Fill mesh trong Edit mode
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action='SELECT')
		bpy.ops.mesh.fill()
		bpy.ops.object.mode_set(mode='OBJECT')

		# Kích hoạt Quadriflow Remesh
		bpy.ops.object.quadriflow_remesh('INVOKE_DEFAULT')

		self.report({'INFO'}, "OK")
		return {'FINISHED'}
	
def register():
	bpy.utils.register_class(SSS_OT_quad_remesh)
def unregister():
	bpy.utils.unregister_class(SSS_OT_quad_remesh)
