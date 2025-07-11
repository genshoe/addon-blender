import bpy

class SSS_OT_apply_lattice(bpy.types.Operator):
	bl_idname = "sss.apply_lattice"
	bl_label = "Apply lattice"
	bl_options = {'REGISTER', 'UNDO'}
		
	def execute(self, context):

		# Đảm bảo đang ở Object Mode
		if bpy.ops.object.mode_set.poll():
			bpy.ops.object.mode_set(mode='OBJECT')
			
		# Bỏ chọn tất cả object
		bpy.ops.object.select_all(action='DESELECT')

		# Lặp qua tất cả các đối tượng trong cảnh
		for obj in context.scene.objects:
			# Kiểm tra đối tượng có phải là đối tượng dạng lưới và có lattice modifier không
			if obj.type == 'MESH':
				context.view_layer.objects.active = obj  # Đặt làm active object

				# Lặp qua các modifier của đối tượng
				for mod in obj.modifiers:
					if mod.type == 'LATTICE':
						try:
							bpy.ops.object.modifier_apply(modifier=mod.name)
						except Exception as e:
							self.report({'WARNING'}, f"Can not apply modifier '{mod.name}' for '{obj.name}'")

		# Lặp và xóa tất cả lattice     
		for lat in context.scene.objects:
				if lat.type == 'LATTICE':
					lat.select_set(True)
					bpy.ops.object.delete()
		# Dọn dẹp
		bpy.ops.outliner.orphans_purge()

		self.report({'INFO'}, "OK")
		return {'FINISHED'}

def register():
	bpy.utils.register_class(SSS_OT_apply_lattice)
def unregister():
	bpy.utils.unregister_class(SSS_OT_apply_lattice)
