import bpy
import os
from mathutils import Vector

import bmesh
import math

def register():
	bpy.utils.register_class(SSS_OT_overlock)
def unregister():
	bpy.utils.unregister_class(SSS_OT_overlock)

class SSS_OT_overlock(bpy.types.Operator):
	bl_idname = "sss.overlock"
	bl_label = "Overlock"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		main(self, context)
		self.report({'INFO'}, "Overlock OK")
		return {'FINISHED'}
	
def main(self, context):

	obj = context.active_object
	if obj is None:
		self.report({'WARNING'}, "Please select an object")
		return {"CANCELLED"}
	if obj.type != "MESH":
		self.report({'WARNING'}, "The selected object is not a mesh")
		return {"CANCELLED"}

	# Tạo UVMap nếu chưa có
	if "UVMap" not in obj.data.uv_layers:
		uvLayer = obj.data.uv_layers.new(name="UVMap")
		obj.data.uv_layers.active = uvLayer
		obj.data.uv_layers["UVMap"].active_render = True

	# Chuyển sang Edit Mode
	bpy.ops.object.mode_set(mode='EDIT')

	# Chọn tất cả
	bpy.ops.mesh.select_all(action='SELECT')

	# UV unwrap
	bpy.ops.uv.unwrap(method='MINIMUM_STRETCH', fill_holes=True, correct_aspect=True, use_subsurf_data=False, margin=0.001, no_flip=False, iterations=10, use_weights=False, weight_group="uv_importance", weight_factor=1)

	# Chọn tất cả mặt uv
	bpy.ops.uv.select_all(action='SELECT')

	# UV rectangle
	bpy.ops.sss.uv_rectangle()

	# UV real size
	bpy.ops.sss.uv_real_size()
	
	#-------------------------------------------------------------------------

	angle_rad = math.radians(180)
	bm = bmesh.from_edit_mesh(obj.data)
	uv_layer = bm.loops.layers.uv.verify()
	selected_uvs = [loop[uv_layer].uv for face in bm.faces if face.select for loop in face.loops if loop[uv_layer].select]
	if selected_uvs:
		center = sum(selected_uvs, Vector((0.0, 0.0))) / len(selected_uvs)
		cos_a = math.cos(angle_rad)
		sin_a = math.sin(angle_rad)
		for uv in selected_uvs:
			offset = uv - center
			uv[:] = center + Vector((
				offset.x * cos_a - offset.y * sin_a,
				offset.x * sin_a + offset.y * cos_a
			))
		bmesh.update_edit_mesh(obj.data)
	#----------------------------------------------------------------------------

	# Trở về Object Mode
	bpy.ops.object.mode_set(mode='OBJECT')

	# Chuyển đổi UV to mesh
	bpy.ops.sss.uv_to_mesh()

	# Lấy object đang active
	overlock2Dbase = context.active_object
	
	# Chuyển bounding box từ local space sang world space
	world_corners = [overlock2Dbase.matrix_world @ Vector(corner) for corner in overlock2Dbase.bound_box]
	
	# 1. Tính chiều dài theo trục Y (world space)
	y_coords = [v.y for v in world_corners]
	y_length = max(y_coords) - min(y_coords)
	
	# 2. Lấy trung điểm của hai điểm đáy (min Z), trái và phải theo trục X
	min_z = min(v.z for v in world_corners)
	bottom_points = [v for v in world_corners if abs(v.z - min_z) < 1e-6]
	left, right = min(bottom_points, key=lambda v: v.x), max(bottom_points, key=lambda v: v.x)
	midpoint = (left + right) / 2

	# Tính xong rồi xóa overlock2Dbase
	bpy.data.objects.remove(overlock2Dbase, do_unlink=True)

	# Dọn dẹp
	bpy.ops.outliner.orphans_purge()

	# Append Overlock object nếu có trong assets
	objAppend = "Overlock"
	if objAppend not in bpy.data.objects:
		# Thư mục hiện tại là GenshoeTools/operators/
		current_dir = os.path.dirname(__file__)
		# Đi lên thư mục GenshoeTools, rồi tới file assets.blend
		blend_path = os.path.normpath(os.path.join(current_dir, "..", "assets.blend"))
		blend_object_dir = os.path.join(blend_path, "Object/")
		bpy.ops.wm.append(
			filepath=os.path.join(blend_object_dir, objAppend),
			directory=blend_object_dir,
			filename=objAppend
		)
	# Gán tọa độ này vào overlock
	overlock = bpy.data.objects.get(objAppend)
	overlock.location = midpoint
	# Đổi tên
	overlock.name = overlock.data.name = "Stitches."+objAppend

	# Apply transform
	context.view_layer.objects.active = overlock
	bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

	# Tính chiều dài theo trục Y của overlock
	world_corners_overlock = [overlock.matrix_world @ Vector(corner) for corner in overlock.bound_box]
	y_coords_overlock = [v.y for v in world_corners_overlock]
	y_length_overlock = max(y_coords_overlock) - min(y_coords_overlock)

	# Tạo Array Modifier
	mod = overlock.modifiers.new(name="Array_Y", type='ARRAY')
	mod.fit_type = 'FIT_LENGTH'
	mod.fit_length = y_length - y_length_overlock # Đơn vị mét
	mod.relative_offset_displace = (0.0, 0.543, 0.0)  # Trục Y
	
	# Tạo modifier Geometry Nodes
	modifier = overlock.modifiers.new("GeometryNodes", "NODES")
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

	i = tree.nodes.new("NodeGroupInput")
	i.location = (-200, 300)
	
	oi = tree.nodes.new("GeometryNodeObjectInfo")
	oi.location = (200, 0)
	oi.transform_space = "RELATIVE"
	oi.inputs[0].default_value = bpy.data.objects[obj.name]
	
	vtr = tree.nodes.new("ShaderNodeVectorMath")
	vtr.location = (800, -400)
	vtr.operation = "SCALE"
	
	mr = tree.nodes.new("ShaderNodeMapRange")
	mr.location = (400, -500)
	mr.data_type = "FLOAT_VECTOR"
	
	sxyz = tree.nodes.new("ShaderNodeSeparateXYZ")
	sxyz.location = (600, -500)
	
	# Tạo socket
	tree.interface.new_socket(name="Geometry", socket_type="NodeSocketGeometry", in_out="INPUT")
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
	tree.links.new(i.outputs["Geometry"], sp.inputs["Geometry"])
	tree.links.new(i.outputs["Geometry"], bb.inputs["Geometry"])

	# Apply từng modifier
	for m in overlock.modifiers:
		bpy.ops.object.modifier_apply(modifier=m.name)

