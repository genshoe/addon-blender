import bpy

def register():
	bpy.utils.register_class(SSS_OT_apply_stitch)
def unregister():
	bpy.utils.unregister_class(SSS_OT_apply_stitch)

class SSS_OT_apply_stitch(bpy.types.Operator):
	bl_idname = "sss.apply_stitch"
	bl_label = "Apply stitch"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		main(self, context)
		self.report({'INFO'}, "OK")
		return {'FINISHED'}
	
def main(self, context):

	# Dọn dẹp
	bpy.ops.outliner.orphans_purge()

	# Đảm bảo đang ở Object Mode
	if bpy.ops.object.mode_set.poll():
		bpy.ops.object.mode_set(mode='OBJECT')
		
	for obj in bpy.context.selected_objects:
		if obj.type == 'MESH':
			bpy.context.view_layer.objects.active = obj  # Đặt làm active để apply
			for modi in obj.modifiers:
				try:
					bpy.ops.object.modifier_apply(modifier=modi.name)
				except Exception as e:
					print(e)
			
			curveName = "Curve" + obj.name[6:]
			obj.name = obj.data.name = "Stitches"+ obj.name[6:]

			if curveName in bpy.data.objects:
				objCurve = bpy.data.objects[curveName]

				# Nếu object đang liên kết trong scene, unlink nó
				for collection in objCurve.users_collection:
					collection.objects.unlink(objCurve)

				# Xóa hoàn toàn object khỏi dữ liệu Blender
				bpy.data.objects.remove(objCurve, do_unlink=True)
	# Dọn dẹp
	bpy.ops.outliner.orphans_purge()
