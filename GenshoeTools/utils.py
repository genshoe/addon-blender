import bpy

def create_collection(collection_name: str, parent_name: str = None) -> bpy.types.Collection:
	"""
	Tạo một collection theo tên và liên kết vào collection cha hoặc scene collection.

	Args:
		collection_name (str): Tên collection muốn tạo.
		parent_name (str, optional): Tên collection cha. Nếu None hoặc không tìm thấy, sẽ link vào scene collection.

	Returns:
		bpy.types.Collection: Collection vừa tạo hoặc đã tồn tại.
	"""

	# Nếu đã tồn tại thì lấy lại
	collection = bpy.data.collections.get(collection_name)
	if collection is None:
		collection = bpy.data.collections.new(collection_name)

	# Tìm collection cha (nếu có)
	parent_collection = bpy.data.collections.get(parent_name) if parent_name else None

	# Kiểm tra đã được liên kết chưa (vào bất kỳ collection nào)
	is_linked = any(collection is child for coll in bpy.data.collections for child in coll.children) or \
				any(collection is child for child in bpy.context.scene.collection.children)

	# Nếu chưa được liên kết thì gắn vào nơi phù hợp
	if not is_linked:
		if parent_collection:
			parent_collection.children.link(collection)
		else:
			bpy.context.scene.collection.children.link(collection)

	return collection

def delete_collection(collection_name: str):
	"""
	Xóa collection và toàn bộ object + collection con (đệ quy).

	Args:
		collection_name (str): Tên collection cần xóa.
	"""
	collection = bpy.data.collections.get(collection_name)
	if not collection:
		print(f"[delete_collection] Collection '{collection_name}' không tồn tại.")
		return

	# 1. Đệ quy xóa tất cả collection con
	for child_collection in list(collection.children):
		delete_collection(child_collection.name)

	# 2. Xóa object trong collection
	for obj in list(collection.objects):
		# Gỡ object khỏi mọi collection
		for coll in list(obj.users_collection):
			coll.objects.unlink(obj)
		# Xoá khỏi data
		bpy.data.objects.remove(obj, do_unlink=True)

	# 3. Gỡ khỏi tất cả scene
	for scene in bpy.data.scenes:
		for child in list(scene.collection.children):
			if child is collection:
				scene.collection.children.unlink(collection)

	# 4. Gỡ khỏi tất cả collection cha
	for parent in bpy.data.collections:
		for child in list(parent.children):
			if child is collection:
				parent.children.unlink(collection)

	# 5. Xóa collection
	bpy.data.collections.remove(collection)
	print(f"[delete_collection] Đã xóa collection '{collection_name}' và toàn bộ nội dung.")

def create_mesh(name: str, parent_collection_name: str = None) -> bpy.types.Object:
	"""
	Tạo một mesh object mới và liên kết vào collection chỉ định hoặc scene collection.

	Args:
		name (str): Tên của object muốn tạo.
		parent_collection_name (str, optional): Tên collection cha để link vào. Nếu không có, sẽ link vào scene collection.

	Returns:
		bpy.types.Object: Object vừa được tạo.
	"""
	# Tạo mesh và object
	mesh_data = bpy.data.meshes.new(name + "_mesh")
	obj = bpy.data.objects.new(name, mesh_data)

	# Tìm collection cha
	target_collection = None
	if parent_collection_name:
		target_collection = bpy.data.collections.get(parent_collection_name)
	
	# Nếu không có collection cha, gán vào scene
	if not target_collection:
		target_collection = bpy.context.scene.collection

	# Link object vào collection
	target_collection.objects.link(obj)

	return obj

def delete_object(name: str):
	"""
	Xóa object theo tên, bao gồm data liên kết và object con (nếu có).

	Args:
		name (str): Tên object muốn xóa.
	"""
	obj = bpy.data.objects.get(name)
	if not obj:
		print(f"[delete_object] Không tìm thấy object '{name}'.")
		return

	# Xử lý object con nếu là parent
	children = [o for o in bpy.data.objects if o.parent == obj]
	for child in children:
		delete_object(child.name)

	# Gỡ object khỏi tất cả collection
	for coll in list(obj.users_collection):
		coll.objects.unlink(obj)

	# Xóa data block nếu không còn dùng nữa
	data = obj.data
	bpy.data.objects.remove(obj, do_unlink=True)

	if data:
		# Kiểm tra không còn object nào dùng chung data nữa
		if hasattr(data, "users") and data.users == 0:
			try:
				bpy.data.meshes.remove(data)
			except:
				try:
					bpy.data.curves.remove(data)
				except:
					try:
						bpy.data.armatures.remove(data)
					except:
						print(f"[delete_object] Không rõ kiểu data của object '{name}', không xóa được.")

	print(f"[delete_object] Đã xóa object '{name}' và data liên quan.")
