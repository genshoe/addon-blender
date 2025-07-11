import bpy

def register():
	bpy.utils.register_class(SSS_OT_create_collection)
def unregister():
	bpy.utils.unregister_class(SSS_OT_create_collection)

class SSS_OT_create_collection(bpy.types.Operator):
	bl_idname = "sss.create_collection"
	bl_label = "Create collection"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if bpy.data.collections.get("2D") is None:
			return True
		else:
			return False

	def execute(self, context):
		main(self, context)
		self.report({'INFO'}, "OK")
		return {'FINISHED'}

def main(self, context):

	for obj in bpy.data.objects:
		bpy.data.objects.remove(obj, do_unlink=True)
	for c in bpy.data.collections:
		bpy.data.collections.remove(c)

	# Tạo light arena
	bpy.ops.object.light_add(type="AREA", location=(0, 0, 2))
	light = bpy.context.active_object
	light.data.energy = 150
	light.data.size = 1
	
	# Tạo collection mới
	cpb = bpy.data.collections.new("Production Base")
	c2d = bpy.data.collections.new("2D")
	c3d = bpy.data.collections.new("3D")
	cshoe = bpy.data.collections.new("Shoe")
	
	# Thêm collection vào scene hiện tại
	bpy.context.scene.collection.children.link(cpb)
	bpy.context.scene.collection.children.link(c2d)
	bpy.context.scene.collection.children.link(c3d)
	bpy.context.scene.collection.children.link(cshoe)
	
	# Tạo một mesh mới
	mesh3d = bpy.data.meshes.new(name="3D_BASE")
	# Tạo một đối tượng mới dùng mesh đó
	obj3d = bpy.data.objects.new("3D_BASE", mesh3d)
	# Thêm object vào scene
	cpb.objects.link(obj3d)
	
	for i in ['Quarter','Quarter_Lining','Collar','Logo','Heel_Piece','Eyestay','Backstay','Toe']:
		mesh = bpy.data.meshes.new(name='2D_'+i)
		obj = bpy.data.objects.new('2D_'+i, mesh)
		c2d.objects.link(obj)
		obj.data.uv_layers.new()
		mdf = obj.modifiers.new(name='Subdivision', type='SUBSURF')
		mdf.levels = 2


