import bpy

class SSS_OT_draw_curve(bpy.types.Operator):
	bl_idname = "sss.draw_curve"
	bl_label = "Draw curve"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		if context.mode.startswith('EDIT'):
			bpy.ops.object.mode_set(mode='OBJECT')
			
		bpy.ops.object.select_all(action='DESELECT')
		curve_data = bpy.data.curves.new(name='DrawCurve', type='CURVE')
		curve_data.dimensions = '3D'
		curve_obj = bpy.data.objects.new('DrawCurve', curve_data)
		context.collection.objects.link(curve_obj)
		context.view_layer.objects.active = curve_obj
		curve_obj.select_set(True)
		bpy.ops.object.mode_set(mode='EDIT')

		for area in context.screen.areas:
			if area.type == 'VIEW_3D':
				with context.temp_override(area=area, region=area.regions[-1]):
					bpy.ops.wm.tool_set_by_id(name="builtin.draw")
					break

		context.scene.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'

		self.report({'INFO'}, "OK")
		return {'FINISHED'}
	
def register():
	bpy.utils.register_class(SSS_OT_draw_curve)
def unregister():
	bpy.utils.unregister_class(SSS_OT_draw_curve)
