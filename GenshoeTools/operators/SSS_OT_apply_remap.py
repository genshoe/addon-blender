import bpy

class SSS_OT_apply_remap(bpy.types.Operator):
	bl_idname = "sss.apply_remap"
	bl_label = "Apply"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		selected = context.selected_objects

		if len(selected) == 0:
			self.report({'WARNING'}, "No objects are selected")
			return {'CANCELLED'}
		
		for check_obj in selected:
			if check_obj.name[:3] != "3D_":
				self.report({'WARNING'}, 'Object name must start with "3D_"')
				return {'CANCELLED'}
			if check_obj.type != 'MESH':
				self.report({'WARNING'}, "The selected object is not a mesh")
				return {'CANCELLED'}

		for obj in selected:
			# Di chuyển 3D_object từ collection "3D" vào collection "Shoe"
			bpy.data.collections.get("3D").objects.unlink(obj)
			bpy.data.collections.get("Shoe").objects.link(obj)

			# Lấy 2D_object theo dựa vào tên của 3D_object
			flat2d = bpy.data.objects.get("2D" + obj.name[2:])

			l = rl = 0
			subd_mod = None

			if flat2d:
				# Tìm modifier subdivision
				subd_mod = next((m for m in flat2d.modifiers if m.type == 'SUBSURF'), None)
				if subd_mod:
					l = subd_mod.levels
					rl = subd_mod.render_levels
					subd_mod.levels = 0
					subd_mod.render_levels = 0

			# Đổi tên 3D_object thành object
			obj.name = obj.data.name = obj.name[3:]

			# Mở khóa transform cho object
			obj.lock_location = (False, False, False)
			obj.lock_rotation = (False, False, False)
			obj.lock_scale = (False, False, False)

			# Active và chọn object, sau đó Apply GeometryNodes 
			context.view_layer.objects.active = obj
			obj.select_set(True)
			if "GeometryNodes" in obj.modifiers:
				bpy.ops.object.mode_set(mode='OBJECT')
				bpy.ops.object.modifier_apply(modifier="GeometryNodes")

			# Gắn lại subdivision nếu 2D object có
			if subd_mod:
				new_subd = obj.modifiers.new(name='Subdivision', type='SUBSURF')
				new_subd.levels = l
				new_subd.render_levels = rl

				# Khôi phục subdivision cho flat2d
				subd_mod.levels = l
				subd_mod.render_levels = rl

		self.report({'INFO'}, "OK apply remap")
		return {'FINISHED'}

def register():
	bpy.utils.register_class(SSS_OT_apply_remap)
def unregister():
	bpy.utils.unregister_class(SSS_OT_apply_remap)
	