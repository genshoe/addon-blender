import bpy
import mathutils

class SSS_OT_add_lattice(bpy.types.Operator):
	bl_idname = "sss.add_lattice"
	bl_label = "Add lattice"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		
		# Lấy danh sách object đang chọn
		selected_objects = context.selected_objects

		if len(selected_objects) == 0:
			self.report({'WARNING'}, "No objects are selected")
			return {'CANCELLED'}
		if all(obj.type != 'MESH' for obj in selected_objects):
			self.report({'WARNING'}, "The selected object is not a mesh")
			return {'CANCELLED'}
				
		# Apply Rotation & Scale để bounding box chính xác
		for obj in selected_objects:
			context.view_layer.objects.active = obj
			bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

		# Tính toán bounding box tổng thể của tất cả object đang chọn
		minBB = mathutils.Vector((float('inf'), float('inf'), float('inf')))
		maxBB = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))

		for obj in selected_objects:
			for corner in obj.bound_box:
				world_corner = obj.matrix_world @ mathutils.Vector(corner)
				minBB = mathutils.Vector((min(minBB[i], world_corner[i]) for i in range(3)))
				maxBB = mathutils.Vector((max(maxBB[i], world_corner[i]) for i in range(3)))

		# Tính tâm và kích thước của lattice
		center = (minBB + maxBB) / 2
		size = maxBB - minBB

		# Tạo lattice object
		bpy.ops.object.add(type='LATTICE', location=center)
		lattice = context.object
		lattice.scale = size
		lattice.data.points_u = 3
		lattice.data.points_v = 3
		lattice.data.points_w = 3

		# Thêm lattice modifier cho từng object
		for obj in selected_objects:
			mod = obj.modifiers.new(name="Lattice", type='LATTICE')
			mod.object = lattice
			
		# Chuyển sang edit mode
		bpy.ops.object.mode_set(mode='EDIT')

		self.report({'INFO'}, "OK")
		return {'FINISHED'}


def register():
	bpy.utils.register_class(SSS_OT_add_lattice)
def unregister():
	bpy.utils.unregister_class(SSS_OT_add_lattice)

