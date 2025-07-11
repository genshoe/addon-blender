import bpy
import bmesh
from mathutils import Vector

class SSS_OT_uv_to_mesh(bpy.types.Operator):
	bl_idname = "sss.uv_to_mesh"
	bl_label = "UV to mesh"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		obj = context.active_object
		if obj is None or obj.type != 'MESH':
			self.report({'WARNING'}, "Please select a mesh")
			return {'CANCELLED'}

		mesh = obj.data
		uv_layer = mesh.uv_layers.active

		bm = bmesh.new()
		bm.from_mesh(mesh)
		uv_layer_bm = bm.loops.layers.uv.active

		verts = []
		faces = []
		vert_map = {}

		for face in bm.faces:
			face_vert_indices = []
			for loop in face.loops:
				uv = loop[uv_layer_bm].uv
				key = (loop.vert.index, loop.index)
				if key not in vert_map:
					vert_map[key] = len(verts)
					verts.append(Vector((uv.x, uv.y, 0.0)))
				face_vert_indices.append(vert_map[key])
			faces.append(face_vert_indices)

		bm.free()

		# Tạo mesh và object mới
		new_mesh = bpy.data.meshes.new("Flat_Base")
		new_mesh.from_pydata(verts, [], faces)
		new_mesh.update()

		new_obj = bpy.data.objects.new(new_mesh.name, new_mesh)
		context.collection.objects.link(new_obj)
		bpy.context.view_layer.objects.active = new_obj

		# Gán UV giống hình học
		new_uv_layer = new_mesh.uv_layers.new(name="UVMap")
		for poly in new_mesh.polygons:
			for loop_index in poly.loop_indices:
				loop = new_mesh.loops[loop_index]
				new_uv_layer.data[loop_index].uv = new_mesh.vertices[loop.vertex_index].co.xy

		# Lấy vật liệu có tên "BaseMaterial"
		material = bpy.data.materials.get("BaseMaterial")

		# Nếu material tồn tại
		if material:
			# Nếu object đã có slot vật liệu, gán vào slot đầu tiên
			if new_obj.data.materials:
				new_obj.data.materials[0] = material
			else:
				# Nếu chưa có slot nào, thêm mới
				new_obj.data.materials.append(material)
		else:
			self.report({'WARNING'}, "Not found BaseMaterial")

		self.report({'INFO'}, "OK UVmap to mesh")
		return {'FINISHED'}

def register():
	bpy.utils.register_class(SSS_OT_uv_to_mesh)
def unregister():
	bpy.utils.unregister_class(SSS_OT_uv_to_mesh)
