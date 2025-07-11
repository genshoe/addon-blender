import bpy
import mathutils

class SSS_OT_set_origin_to_bottom(bpy.types.Operator):
	bl_idname = "sss.set_origin_to_bottom"
	bl_label = "Set origin to bottom"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		# Lấy object đang được chọn
		obj = context.active_object

		if obj is None:
			self.report({'WARNING'}, "No object are active")
			return {'CANCELLED'}
		if obj.type != 'MESH':
			self.report({'WARNING'}, "The selected object is not a mesh")
			return {'CANCELLED'}

		# Apply Rotation
		bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

		# Tính bounding box trong local space
		bbox = [mathutils.Vector(corner) for corner in obj.bound_box]

		# Tính trung tâm X, Y và Z thấp nhất
		center_x = sum(v[0] for v in bbox) / 8
		center_y = sum(v[1] for v in bbox) / 8
		min_z = min(v[2] for v in bbox)

		# Vị trí trung tâm đáy trong local space
		bottom_center_local = mathutils.Vector((center_x, center_y, min_z))

		# Chuyển sang tọa độ thế giới
		bottom_center= obj.matrix_world @ bottom_center_local

		# Đặt 3D Cursor vào vị trí này
		context.scene.cursor.location = bottom_center

		# Đặt Origin về 3D Cursor
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

		self.report({'INFO'}, "OK")
		return {'FINISHED'}

def register():
	bpy.utils.register_class(SSS_OT_set_origin_to_bottom)
def unregister():
	bpy.utils.unregister_class(SSS_OT_set_origin_to_bottom)
	

