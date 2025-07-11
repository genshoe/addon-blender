import bpy

class SSS_OT_config_file(bpy.types.Operator):
	bl_idname = "sss.config_file"
	bl_label = "Config file"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		main(self, context)
		self.report({'INFO'}, "Config file OK")
		return {'FINISHED'}
	
def main(self, context):
	
	if not bpy.data.use_autopack:
		bpy.data.use_autopack = True
	
	context.scene.unit_settings.length_unit = "MILLIMETERS"
	context.preferences.inputs.use_mouse_emulate_3_button = True
	context.preferences.inputs.use_zoom_to_mouse = True
	context.scene.view_settings.view_transform = "Khronos PBR Neutral"
	
	context.scene.render.fps = 30
	context.scene.render.engine = "CYCLES"
	context.scene.cycles.device = "GPU"
	
	# Lấy preferences cho addon "cycles"
	#cycles_prefs = context.preferences.addons["cycles"].preferences
	
	# Chọn thiết bị tính toán là CUDA
	#cycles_prefs.compute_device_type = "CUDA"
	
	# Bật tất cả GPU có sẵn
	#for device in cycles_prefs.get_devices()[0]:
	#    device.use = True
	
	context.scene.cycles.preview_samples = 64
	context.scene.cycles.samples = 256

def register():
	bpy.utils.register_class(SSS_OT_config_file)
def unregister():
	bpy.utils.unregister_class(SSS_OT_config_file)

