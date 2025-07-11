import bpy
import bmesh
from mathutils import Vector


class SSS_OT_uv_real_size(bpy.types.Operator):
	bl_idname = "sss.uv_real_size"
	bl_label = "UV real size"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		'''
		if not context.active_object:
			return False
		if context.active_object.mode != 'EDIT':
			return False
		if context.active_object.type != 'MESH':
			return False
		if not context.object.data.uv_layers:
			return False
		if context.scene.tool_settings.use_uv_select_sync:
			return False
		'''

		obj = context.object

		bpy.ops.object.mode_set(mode='EDIT')
		bm = bmesh.from_edit_mesh(obj.data)
		uv_layer = bm.loops.layers.uv.verify()

		total_3d_len = 0.0
		total_uv_len = 0.0
		all_uvs = []

		for face in bm.faces:
			if not face.select:
				continue

			loops = face.loops
			for i in range(len(loops)):
				loop1 = loops[i]
				loop2 = loops[(i + 1) % len(loops)]

				uv1 = loop1[uv_layer].uv
				uv2 = loop2[uv_layer].uv
				v1 = loop1.vert.co
				v2 = loop2.vert.co

				total_3d_len += (v2 - v1).length
				total_uv_len += (uv2 - uv1).length

				all_uvs.append(uv1)

		if total_uv_len == 0.0 or total_3d_len == 0.0:
			self.report({'ERROR'}, "Mesh or UVs have zero length (check unwrap status)")
			return {'CANCELLED'}

		scale_ratio = total_3d_len / total_uv_len
		center = sum(all_uvs, Vector((0.0, 0.0))) / len(all_uvs)

		for face in bm.faces:
			if not face.select:
				continue
			for loop in face.loops:
				uv = loop[uv_layer].uv
				uv[:] = (uv - center) * scale_ratio + center

		bmesh.update_edit_mesh(obj.data)
		
		self.report({'INFO'}, "OK UV real size")
		return {'FINISHED'}

def register():
	bpy.utils.register_class(SSS_OT_uv_real_size)
def unregister():
	bpy.utils.unregister_class(SSS_OT_uv_real_size)

