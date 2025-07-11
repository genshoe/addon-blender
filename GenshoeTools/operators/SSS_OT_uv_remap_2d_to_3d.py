import bpy

class SSS_OT_uv_remap_2d_to_3d(bpy.types.Operator):
	bl_idname = "sss.uv_remap_2d_to_3d"
	bl_label = "UV remap"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		main(self, context)
		self.report({'INFO'}, "OK UV remap")
		return {'FINISHED'}

def main(self, context):


	selected_objects = context.selected_objects

	if len(selected_objects) == 0:
		self.report({'WARNING'}, "No objects are selected")
		return {'CANCELLED'}
	
	for check_obj in selected_objects:
		if check_obj.name[:3] != "2D_":
			self.report({'WARNING'}, 'Object name must start with "2D_"')
			return {'CANCELLED'}
		if check_obj.type != 'MESH':
			self.report({'WARNING'}, "The selected object is not a mesh")
			return {'CANCELLED'}

	# Dọn dẹp
	bpy.ops.outliner.orphans_purge()

	# Bỏ chọn tất cả
	bpy.ops.object.select_all(action='DESELECT')

	for objActive in selected_objects:

		newName = "3D"+objActive.name[2:]
		
		# Tạo một mesh rỗng mới
		mesh = bpy.data.meshes.new(name=newName)
		# Tạo một object mới chứa mesh đó
		obj = bpy.data.objects.new(name=newName, object_data=mesh)
		# Di chuyển mesh đó vào collection tên là 3D
		bpy.data.collections.get("3D").objects.link(obj)
		
		# Khóa transform
		obj.lock_location = (True, True, True)
		obj.lock_rotation = (True, True, True)
		obj.lock_scale = (True, True, True)

		obj.select_set(True)     

		# Tạo modifier Geometry Nodes
		modifier = obj.modifiers.new("GeometryNodes", "NODES")
		# Tạo Geometry Node Tree mới
		tree = bpy.data.node_groups.new("NodeTree", "GeometryNodeTree")
		# Gán node tree vào modifier
		modifier.node_group = tree
		
		
		# Thêm node vào node tree	
		sp = tree.nodes.new("GeometryNodeSetPosition")
		sp.location = (1000, 0)
		
		p = tree.nodes.new("GeometryNodeInputPosition")
		p.location = (200, -300)
		
		sus = tree.nodes.new("GeometryNodeSampleUVSurface")
		sus.location = (600, 0)
		sus.data_type = "FLOAT_VECTOR"
		
		sus2 = tree.nodes.new("GeometryNodeSampleUVSurface")
		sus2.location = (600, -250)
		sus2.data_type = "FLOAT_VECTOR"
		
		n = tree.nodes.new("GeometryNodeInputNormal")
		n.location = (200, -200)
		
		bb = tree.nodes.new("GeometryNodeBoundBox")
		bb.location = (200, -600)
		
		na = tree.nodes.new("GeometryNodeInputNamedAttribute")
		na.location = (200, -400)
		na.data_type = "FLOAT_VECTOR"
		na.inputs[0].default_value = "UVMap"
		
		o = tree.nodes.new("NodeGroupOutput")
		o.location = (1200, 0)
		
		oi = tree.nodes.new("GeometryNodeObjectInfo")
		oi.location = (200, 0)
		oi.inputs[0].default_value = bpy.data.objects["3D_BASE"]
		
		oi2 = tree.nodes.new("GeometryNodeObjectInfo")
		oi2.location = (-200, -300)
		oi2.inputs[0].default_value = bpy.data.objects[objActive.name]
		oi2.transform_space = "RELATIVE"
		
		vtr = tree.nodes.new("ShaderNodeVectorMath")
		vtr.location = (800, -400)
		vtr.operation = "SCALE"
		
		mr = tree.nodes.new("ShaderNodeMapRange")
		mr.location = (400, -500)
		mr.data_type = "FLOAT_VECTOR"
		
		sxyz = tree.nodes.new("ShaderNodeSeparateXYZ")
		sxyz.location = (600, -500)
		
		# Tạo socket
		tree.interface.new_socket(name="Geometry", socket_type="NodeSocketGeometry", in_out="OUTPUT")
		
		# Tạo liên kết giữa các node
		tree.links.new(sp.outputs["Geometry"], o.inputs["Geometry"])
		
		tree.links.new(na.outputs["Attribute"], sus.inputs["UV Map"])
		tree.links.new(na.outputs["Attribute"], sus2.inputs["UV Map"])
		
		tree.links.new(sus.outputs["Value"], sp.inputs["Position"])
		tree.links.new(sus.outputs["Value"], vtr.inputs["Vector"])
		tree.links.new(sus2.outputs["Value"], vtr.inputs["Vector"])
		
		tree.links.new(bb.outputs["Min"], mr.inputs["From Min"])
		tree.links.new(bb.outputs["Min"], mr.inputs["To Min"])
		tree.links.new(bb.outputs["Max"], mr.inputs["From Max"])
		tree.links.new(bb.outputs["Max"], mr.inputs["To Max"])
		
		tree.links.new(mr.outputs["Vector"], sxyz.inputs["Vector"])
		tree.links.new(mr.outputs["Vector"], sus.inputs["Sample UV"])
		
		tree.links.new(p.outputs["Position"], mr.inputs["Vector"])
		tree.links.new(p.outputs["Position"], sus.inputs["Value"])
		tree.links.new(p.outputs["Position"], sus2.inputs["Sample UV"])
		
		tree.links.new(n.outputs["Normal"], sus2.inputs["Value"])
		
		tree.links.new(sxyz.outputs["Z"], vtr.inputs["Scale"])
		
		tree.links.new(vtr.outputs["Vector"], sp.inputs["Offset"])
		
		tree.links.new(oi.outputs["Geometry"], sus.inputs["Mesh"])
		tree.links.new(oi.outputs["Geometry"], sus2.inputs["Mesh"])
		tree.links.new(oi2.outputs["Geometry"], sp.inputs["Geometry"])
		tree.links.new(oi2.outputs["Geometry"], bb.inputs["Geometry"])


def register():
	bpy.utils.register_class(SSS_OT_uv_remap_2d_to_3d)
def unregister():
	bpy.utils.unregister_class(SSS_OT_uv_remap_2d_to_3d)
