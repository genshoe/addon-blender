import bpy

class SSS_OT_bake(bpy.types.Operator):
	bl_idname = "sss.bake"
	bl_label = "Bake"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		selected = context.selected_objects
		if len(selected) != 2 or all(obj.type != 'MESH' for obj in selected):
			self.report({'WARNING'}, "Please select 2 objects")
			return {'CANCELLED'}

		# Đảm bảo render engine là Cycles
		context.scene.render.engine = 'CYCLES'

		# Lấy object active (low poly) và selected (high poly)

		low_poly = context.active_object
		high_poly = None
		for obj in selected:
			if obj != low_poly:
				high_poly = obj
				break

		# Đảm bảo object ở object mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# Apply transform cho cả 2
		for obj in [low_poly, high_poly]:
			context.view_layer.objects.active = obj
			bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

		# Tạo vật liệu mới và gán vào low_poly
		material = bpy.data.materials.new(name="BakeMaterial")
		material.use_nodes = True
		low_poly.data.materials.clear()
		low_poly.data.materials.append(material)

		# Đảm bảo có UV Map
		if not low_poly.data.uv_layers:
			low_poly.data.uv_layers.new(name="UVMap")

		# Tạo ảnh mới và node ảnh
		image = bpy.data.images.new("BakeTexture", width=4096, height=4096)

		nodes = material.node_tree.nodes
		links = material.node_tree.links

		# Xóa node cũ (giữ lại output)
		for node in nodes:
			if node.type != 'OUTPUT_MATERIAL':
				nodes.remove(node)

		# Thêm BSDF và Image Texture
		bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
		bsdf.location = (0, 300)
		bsdf.inputs["Roughness"].default_value = 1


		image_node = nodes.new(type='ShaderNodeTexImage')
		image_node.location = (-300, 300)
		image_node.image = image

		# Kết nối Image -> Base Color
		links.new(image_node.outputs['Color'], bsdf.inputs['Base Color'])

		# Kết nối BSDF -> Output
		output = nodes.get("Material Output")
		links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

		# Set Image Texture node là active để bake
		nodes.active = image_node

		# Chọn lại object
		bpy.ops.object.select_all(action='DESELECT')
		high_poly.select_set(True)
		low_poly.select_set(True)
		context.view_layer.objects.active = low_poly

		# Thiết lập bake
		scene = context.scene
		scene.cycles.bake_type = 'DIFFUSE'
		scene.render.bake.use_pass_direct = False
		scene.render.bake.use_pass_indirect = False
		scene.render.bake.use_selected_to_active = True
		scene.render.bake.cage_extrusion = 0.03

		# Bake!
		bpy.ops.object.bake(type='DIFFUSE')

		self.report({'INFO'}, "OK")
		return {'FINISHED'}

def register():
	bpy.utils.register_class(SSS_OT_bake)
def unregister():
	bpy.utils.unregister_class(SSS_OT_bake)

