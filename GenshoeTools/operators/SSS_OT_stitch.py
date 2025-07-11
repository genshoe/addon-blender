import bpy
import os

def register():
	bpy.utils.register_class(SSS_OT_stitch)
def unregister():
	bpy.utils.unregister_class(SSS_OT_stitch)

class SSS_OT_stitch(bpy.types.Operator):
	bl_idname = "sss.stitch"
	bl_label = "Stitch"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		main(self, context)
		self.report({'INFO'}, "OK")
		return {'FINISHED'}

def main(self, context):
	check = context.active_object
	if not check:
		return {'CANCELLED'}
	if check.mode != 'EDIT':
		return {'CANCELLED'}


	# Dọn dẹp
	bpy.ops.outliner.orphans_purge()

	# Duplicate cạnh
	bpy.ops.mesh.duplicate()
	# Tách phần mới bằng loose parts
	bpy.ops.mesh.separate(type='LOOSE')
	# Quay lại Object Mode để xử lý object mới
	bpy.ops.object.mode_set(mode='OBJECT')

	selected_objects = bpy.context.selected_objects
	active_object = bpy.context.active_object

	# Lọc ra các object được chọn nhưng không phải là active
	selected = [obj for obj in selected_objects if obj != active_object]

	listSelect = []

	# Append stitch object nếu có trong assets
	if "Stitch" not in bpy.data.objects:
		# Thư mục hiện tại là GenshoeTools/operators/
		current_dir = os.path.dirname(__file__)
		# Đi lên thư mục GenshoeTools, rồi tới file assets.blend
		blend_path = os.path.normpath(os.path.join(current_dir, "..", "assets.blend"))
		blend_object_dir = os.path.join(blend_path, "Object/")
		bpy.ops.wm.append(
			filepath=os.path.join(blend_object_dir, "Stitch"),
			directory=blend_object_dir,
			filename="Stitch"
		)

	for newCurve in selected:
		# Bỏ chọn tất cả
		bpy.ops.object.select_all(action='DESELECT')

		# Chọn làm active
		newCurve.select_set(True)
		bpy.context.view_layer.objects.active = newCurve

		# Thêm modifier Subdivision
		newCurve.modifiers.new(name='Subdivision', type='SUBSURF')  
		newCurve.modifiers["Subdivision"].levels = 2
		bpy.ops.object.modifier_apply(modifier="Subdivision")

		# Convert to curve
		bpy.ops.object.convert(target='CURVE')

		# Đổi tên curve
		newCurve.name = newCurve.data.name = "Curve."+bpy.context.active_object.name
		
		# them ten mesh vao list de mot chut chon
		listSelect.append(newCurve.name)
		
		#=======================================================================================================
		# Tạo mesh mới
		newStitchMesh = bpy.data.meshes.new(name='Stitch'+newCurve.name[5:])
		# Tạo một object mới chứa mesh đó
		newStitchObject = bpy.data.objects.new(name=newStitchMesh.name, object_data=newStitchMesh)
		
		# Thêm tên vào list để một chút chọn
		listSelect.append(newStitchObject.name)
		
		# Chuyển object vào scene
		#bpy.data.collections.get("Collection").objects.link(newStitchObject)
		bpy.context.scene.collection.objects.link(newStitchObject)
		# Chọn và active
		newStitchObject.select_set(True)
		bpy.context.view_layer.objects.active = newStitchObject

		# newStitchObject = bpy.context.active_object
		# Tạo modifier Geometry Nodes
		geoModifier = newStitchObject.modifiers.new("Geometry", "NODES")
		# Tạo Geometry Node Tree mới
		nodetree = bpy.data.node_groups.new("NodeTree", "GeometryNodeTree")
		# Gán node tree vào modifier
		geoModifier.node_group = nodetree

		#==========================Tạo nodes -=========================================


		#nodetree interface
		#Socket Geometry
		geometry_socket = nodetree.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
		geometry_socket.attribute_domain = 'POINT'

		#Socket Curve object
		curve_object_socket = nodetree.interface.new_socket(name = "Curve object", in_out='INPUT', socket_type = 'NodeSocketObject')
		curve_object_socket.attribute_domain = 'POINT'

		#Socket Stitch object
		stitch_object_socket = nodetree.interface.new_socket(name = "Stitch object", in_out='INPUT', socket_type = 'NodeSocketObject')
		stitch_object_socket.attribute_domain = 'POINT'

		#Socket Rotation
		rotation_socket = nodetree.interface.new_socket(name = "Rotation", in_out='INPUT', socket_type = 'NodeSocketFloat')
		rotation_socket.default_value = 0.0
		rotation_socket.min_value = 0.0
		rotation_socket.max_value = 6.3
		rotation_socket.subtype = 'NONE'
		rotation_socket.attribute_domain = 'POINT'

		#Socket Offset
		offset_socket = nodetree.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketFloat')
		offset_socket.default_value = 0.0
		offset_socket.min_value = -0.001
		offset_socket.max_value = 0.001
		offset_socket.subtype = 'FACTOR'
		offset_socket.default_attribute_name = "0"
		offset_socket.attribute_domain = 'POINT'

		#Socket Gap
		gap_socket = nodetree.interface.new_socket(name = "Gap", in_out='INPUT', socket_type = 'NodeSocketFloat')
		gap_socket.default_value = 0.0
		gap_socket.min_value = 0.001
		gap_socket.max_value = 2.0
		gap_socket.subtype = 'NONE'
		gap_socket.default_attribute_name = "0"
		gap_socket.attribute_domain = 'POINT'

		#Socket Zig-zag
		zig_zag_socket = nodetree.interface.new_socket(name = "Zig-zag", in_out='INPUT', socket_type = 'NodeSocketInt')
		zig_zag_socket.default_value = 0
		zig_zag_socket.min_value = 0
		zig_zag_socket.max_value = 90
		zig_zag_socket.subtype = 'NONE'
		zig_zag_socket.attribute_domain = 'POINT'
		zig_zag_socket.force_non_field = True

		#Socket Scale
		scale_socket = nodetree.interface.new_socket(name = "Scale", in_out='INPUT', socket_type = 'NodeSocketVector')
		scale_socket.default_value = (1.0, 1.0, 1.0)
		scale_socket.min_value = 0.1
		scale_socket.max_value = 2.0
		scale_socket.subtype = 'XYZ'
		scale_socket.attribute_domain = 'POINT'
		scale_socket.force_non_field = True


		#initialize nodetree nodes
		#node Group Input
		group_input = nodetree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Group Output
		group_output = nodetree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Object Info
		object_info = nodetree.nodes.new("GeometryNodeObjectInfo")
		object_info.name = "Object Info"
		object_info.transform_space = 'ORIGINAL'
		#As Instance
		object_info.inputs[1].default_value = False

		#node Instance on Points
		instance_on_points = nodetree.nodes.new("GeometryNodeInstanceOnPoints")
		instance_on_points.name = "Instance on Points"
		#Selection
		instance_on_points.inputs[1].default_value = True
		#Pick Instance
		instance_on_points.inputs[3].default_value = False
		#Instance Index
		instance_on_points.inputs[4].default_value = 0

		#node Realize Instances
		realize_instances = nodetree.nodes.new("GeometryNodeRealizeInstances")
		realize_instances.name = "Realize Instances"

		#node Object Info.001
		object_info_001 = nodetree.nodes.new("GeometryNodeObjectInfo")
		object_info_001.name = "Object Info.001"
		object_info_001.transform_space = 'ORIGINAL'
		#As Instance
		object_info_001.inputs[1].default_value = False

		#node Curve Length
		curve_length = nodetree.nodes.new("GeometryNodeCurveLength")
		curve_length.name = "Curve Length"

		#node Mesh Line
		mesh_line = nodetree.nodes.new("GeometryNodeMeshLine")
		mesh_line.name = "Mesh Line"
		mesh_line.count_mode = 'TOTAL'
		mesh_line.mode = 'OFFSET'
		#Start Location
		mesh_line.inputs[2].default_value = (0.0015, 0.0, 0.0)

		#node Math
		math = nodetree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'DIVIDE'
		math.use_clamp = False

		#node Bounding Box
		bounding_box = nodetree.nodes.new("GeometryNodeBoundBox")
		bounding_box.name = "Bounding Box"

		#node Separate XYZ
		separate_xyz = nodetree.nodes.new("ShaderNodeSeparateXYZ")
		separate_xyz.name = "Separate XYZ"

		#node Math.001
		math_001 = nodetree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'SUBTRACT'
		math_001.use_clamp = False

		#node Float to Integer
		float_to_integer = nodetree.nodes.new("FunctionNodeFloatToInt")
		float_to_integer.name = "Float to Integer"
		float_to_integer.rounding_mode = 'ROUND'

		#node Bounding Box.001
		bounding_box_001 = nodetree.nodes.new("GeometryNodeBoundBox")
		bounding_box_001.name = "Bounding Box.001"

		#node Separate XYZ.001
		separate_xyz_001 = nodetree.nodes.new("ShaderNodeSeparateXYZ")
		separate_xyz_001.name = "Separate XYZ.001"

		#node Combine XYZ
		combine_xyz = nodetree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz.name = "Combine XYZ"
		#Y
		combine_xyz.inputs[1].default_value = 0.0
		#Z
		combine_xyz.inputs[2].default_value = 0.0

		#node Transform Geometry.001
		transform_geometry_001 = nodetree.nodes.new("GeometryNodeTransform")
		transform_geometry_001.name = "Transform Geometry.001"
		#Translation
		transform_geometry_001.inputs[1].default_value = (0.0, 0.0, 0.0)

		#node Combine XYZ.001
		combine_xyz_001 = nodetree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_001.name = "Combine XYZ.001"
		#Y
		combine_xyz_001.inputs[1].default_value = 1.0
		#Z
		combine_xyz_001.inputs[2].default_value = 1.0

		#node Combine XYZ.002
		combine_xyz_002 = nodetree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_002.name = "Combine XYZ.002"
		#X
		combine_xyz_002.inputs[0].default_value = 0.0
		#Y
		combine_xyz_002.inputs[1].default_value = 0.0

		#node Combine XYZ.003
		combine_xyz_003 = nodetree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_003.name = "Combine XYZ.003"
		#Y
		combine_xyz_003.inputs[1].default_value = 0.0
		#Z
		combine_xyz_003.inputs[2].default_value = 0.0

		#node Index
		index = nodetree.nodes.new("GeometryNodeInputIndex")
		index.name = "Index"

		#node Math.002
		math_002 = nodetree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MODULO'
		math_002.use_clamp = False
		#Value_001
		math_002.inputs[1].default_value = 2.0

		#node Math.003
		math_003 = nodetree.nodes.new("ShaderNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'MULTIPLY'
		math_003.use_clamp = False
		#Value_001
		math_003.inputs[1].default_value = 2.0

		#node Math.004
		math_004 = nodetree.nodes.new("ShaderNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'SUBTRACT'
		math_004.use_clamp = False
		#Value_001
		math_004.inputs[1].default_value = 1.0

		#node Math.005
		math_005 = nodetree.nodes.new("ShaderNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'MULTIPLY'
		math_005.use_clamp = False

		#node Math.006
		math_006 = nodetree.nodes.new("ShaderNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'DIVIDE'
		math_006.use_clamp = False
		#Value_001
		math_006.inputs[1].default_value = 1000000.0

		#node Combine XYZ.004
		combine_xyz_004 = nodetree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_004.name = "Combine XYZ.004"
		#X
		combine_xyz_004.inputs[0].default_value = 0.0
		#Y
		combine_xyz_004.inputs[1].default_value = 0.0

		#node Math.007
		math_007 = nodetree.nodes.new("ShaderNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'MULTIPLY'
		math_007.use_clamp = False

		#node Value
		value = nodetree.nodes.new("ShaderNodeValue")
		value.name = "Value"

		value.outputs[0].default_value = 17453.0
		#node Transform Geometry.002
		transform_geometry_002 = nodetree.nodes.new("GeometryNodeTransform")
		transform_geometry_002.name = "Transform Geometry.002"
		#Scale
		transform_geometry_002.inputs[3].default_value = (1.0, 1.0, 1.0)




		#Set locations
		group_input.location = (-1680.0, -320.0)
		group_output.location = (640.0, 20.0)
		object_info.location = (-1440.0, 260.0)
		instance_on_points.location = (100.0, 200.0)
		realize_instances.location = (460.0, 20.0)
		object_info_001.location = (-1440.0, 520.0)
		curve_length.location = (-640.0, 580.0)
		mesh_line.location = (-80.0, 480.0)
		math.location = (-440.0, 580.0)
		bounding_box.location = (-980.0, 440.0)
		separate_xyz.location = (-820.0, 440.0)
		math_001.location = (-640.0, 460.0)
		float_to_integer.location = (-240.0, 480.0)
		bounding_box_001.location = (-980.0, 300.0)
		separate_xyz_001.location = (-820.0, 300.0)
		combine_xyz.location = (-440.0, 400.0)
		transform_geometry_001.location = (-1160.0, 380.0)
		combine_xyz_001.location = (-1440.0, -240.0)
		combine_xyz_002.location = (-1440.0, -100.0)
		combine_xyz_003.location = (-1440.0, 40.0)
		index.location = (-1120.0, -660.0)
		math_002.location = (-960.0, -600.0)
		math_003.location = (-800.0, -600.0)
		math_004.location = (-640.0, -600.0)
		math_005.location = (-460.0, -320.0)
		math_006.location = (-960.0, -440.0)
		combine_xyz_004.location = (-280.0, -320.0)
		math_007.location = (-640.0, -320.0)
		value.location = (-1120.0, -500.0)
		transform_geometry_002.location = (280.0, 20.0)

		#initialize nodetree links
		#group_input.Stitch object -> object_info.Object
		nodetree.links.new(group_input.outputs[1], object_info.inputs[0])
		#mesh_line.Mesh -> instance_on_points.Points
		nodetree.links.new(mesh_line.outputs[0], instance_on_points.inputs[0])
		#separate_xyz.X -> math_001.Value
		nodetree.links.new(separate_xyz.outputs[0], math_001.inputs[0])
		#separate_xyz_001.X -> math_001.Value
		nodetree.links.new(separate_xyz_001.outputs[0], math_001.inputs[1])
		#float_to_integer.Integer -> mesh_line.Resolution
		nodetree.links.new(float_to_integer.outputs[0], mesh_line.inputs[1])
		#bounding_box.Max -> separate_xyz.Vector
		nodetree.links.new(bounding_box.outputs[2], separate_xyz.inputs[0])
		#bounding_box_001.Min -> separate_xyz_001.Vector
		nodetree.links.new(bounding_box_001.outputs[1], separate_xyz_001.inputs[0])
		#math_001.Value -> math.Value
		nodetree.links.new(math_001.outputs[0], math.inputs[1])
		#curve_length.Length -> math.Value
		nodetree.links.new(curve_length.outputs[0], math.inputs[0])
		#math.Value -> float_to_integer.Float
		nodetree.links.new(math.outputs[0], float_to_integer.inputs[0])
		#transform_geometry_002.Geometry -> realize_instances.Geometry
		nodetree.links.new(transform_geometry_002.outputs[0], realize_instances.inputs[0])
		#transform_geometry_001.Geometry -> bounding_box.Geometry
		nodetree.links.new(transform_geometry_001.outputs[0], bounding_box.inputs[0])
		#object_info_001.Geometry -> curve_length.Curve
		nodetree.links.new(object_info_001.outputs[3], curve_length.inputs[0])
		#object_info.Geometry -> transform_geometry_001.Geometry
		nodetree.links.new(object_info.outputs[3], transform_geometry_001.inputs[0])
		#transform_geometry_001.Geometry -> bounding_box_001.Geometry
		nodetree.links.new(transform_geometry_001.outputs[0], bounding_box_001.inputs[0])
		#combine_xyz.Vector -> mesh_line.Offset
		nodetree.links.new(combine_xyz.outputs[0], mesh_line.inputs[3])
		#math_001.Value -> combine_xyz.X
		nodetree.links.new(math_001.outputs[0], combine_xyz.inputs[0])
		#combine_xyz_001.Vector -> transform_geometry_001.Scale
		nodetree.links.new(combine_xyz_001.outputs[0], transform_geometry_001.inputs[3])
		#float_to_integer.Integer -> mesh_line.Count
		nodetree.links.new(float_to_integer.outputs[0], mesh_line.inputs[0])
		#group_input.Gap -> combine_xyz_001.X
		nodetree.links.new(group_input.outputs[4], combine_xyz_001.inputs[0])
		#group_input.Offset -> combine_xyz_002.Z
		nodetree.links.new(group_input.outputs[3], combine_xyz_002.inputs[2])
		#combine_xyz_003.Vector -> transform_geometry_001.Rotation
		nodetree.links.new(combine_xyz_003.outputs[0], transform_geometry_001.inputs[2])
		#index.Index -> math_002.Value
		nodetree.links.new(index.outputs[0], math_002.inputs[0])
		#math_002.Value -> math_003.Value
		nodetree.links.new(math_002.outputs[0], math_003.inputs[0])
		#math_003.Value -> math_004.Value
		nodetree.links.new(math_003.outputs[0], math_004.inputs[0])
		#math_005.Value -> combine_xyz_004.Z
		nodetree.links.new(math_005.outputs[0], combine_xyz_004.inputs[2])
		#combine_xyz_004.Vector -> instance_on_points.Rotation
		nodetree.links.new(combine_xyz_004.outputs[0], instance_on_points.inputs[5])
		#value.Value -> math_006.Value
		nodetree.links.new(value.outputs[0], math_006.inputs[0])
		#instance_on_points.Instances -> transform_geometry_002.Geometry
		nodetree.links.new(instance_on_points.outputs[0], transform_geometry_002.inputs[0])
		#combine_xyz_003.Vector -> transform_geometry_002.Rotation
		nodetree.links.new(combine_xyz_003.outputs[0], transform_geometry_002.inputs[2])
		#math_006.Value -> math_007.Value
		nodetree.links.new(math_006.outputs[0], math_007.inputs[1])
		#math_007.Value -> math_005.Value
		nodetree.links.new(math_007.outputs[0], math_005.inputs[0])
		#math_004.Value -> math_005.Value
		nodetree.links.new(math_004.outputs[0], math_005.inputs[1])
		#realize_instances.Geometry -> group_output.Geometry
		nodetree.links.new(realize_instances.outputs[0], group_output.inputs[0])
		#object_info.Geometry -> instance_on_points.Instance
		nodetree.links.new(object_info.outputs[3], instance_on_points.inputs[2])
		#combine_xyz_002.Vector -> transform_geometry_002.Translation
		nodetree.links.new(combine_xyz_002.outputs[0], transform_geometry_002.inputs[1])
		#group_input.Scale -> instance_on_points.Scale
		nodetree.links.new(group_input.outputs[6], instance_on_points.inputs[6])
		#group_input.Rotation -> combine_xyz_003.X
		nodetree.links.new(group_input.outputs[2], combine_xyz_003.inputs[0])
		#group_input.Zig-zag -> math_007.Value
		nodetree.links.new(group_input.outputs[5], math_007.inputs[0])
		#group_input.Curve object -> object_info_001.Object
		nodetree.links.new(group_input.outputs[0], object_info_001.inputs[0])



		# Đặt giá trị cho modifier geometry
		bpy.ops.object.modifier_set_active(modifier="Geometry")
		bpy.context.object.modifiers["Geometry"]["Socket_1"] = bpy.data.objects[newCurve.name]
		bpy.context.object.modifiers["Geometry"]["Socket_2"] = bpy.data.objects["Stitch"]
		bpy.context.object.modifiers["Geometry"]["Socket_5"] = 1.0
		bpy.context.object.modifiers["Geometry"]["Socket_7"] = (1.0,1.0,1.0)



		# ============== Thêm Curve modifier =======================================
		curveModifier = newStitchObject.modifiers.new(name='Curve', type='CURVE')
		curveModifier.object = newCurve

		# Đặt geoModifier làm active
		bpy.ops.object.modifier_set_active(modifier="Geometry")

	# Bỏ chọn tất cả
	bpy.ops.object.select_all(action='DESELECT')

	# Lặp qua danh sách và chọn object tương ứng
	for n in listSelect:
		select_obj = bpy.data.objects.get(n)
		if select_obj:
			select_obj.select_set(True)