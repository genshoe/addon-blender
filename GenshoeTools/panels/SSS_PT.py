import bpy

class SSS_PT_MAIN(bpy.types.Panel):
	bl_label = "Genshoe tools"
	bl_idname = "SSS_PT_MAIN"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Genshoe"
	
	def draw(self, context):
		layout = self.layout
		layout.label(text=f"Edge length: {context.scene.edge_length_props.edge_total_length_mm:.2f} mm")

		row7 = layout.row()
		row7.operator("sss.config_file", icon='TOOL_SETTINGS')
		row7.operator("sss.create_collection", icon='OUTLINER_OB_GROUP_INSTANCE')

		layout.operator("sss.studio", icon='SCENE_DATA')
		layout.operator("sss.set_origin_to_bottom", icon='TRACKER')



		row6 = layout.row()
		row6.operator("sss.bake", icon='RENDER_STILL')
		row6.operator("sss.uv_to_mesh", icon='MESH_GRID')

		row1 = layout.row()
		row1s1 = row1.split(factor=0.6, align=True)
		row1s1.operator("sss.uv_remap_2d_to_3d", text='UV remap', icon='LOOP_BACK')
		row1s2 = row1s1.split(align=True)
		row1s2.operator("sss.apply_remap", text='Apply')

		row2 = layout.row()
		row2s1 = row2.split(factor=0.6, align=True)
		row2s1.operator("sss.add_lattice", text='Lattice', icon='MOD_LATTICE')
		row2s2 = row2s1.split(align=True)
		row2s2.operator("sss.apply_lattice", text='Apply')

		row3 = layout.row()
		row3s1 = row3.split(factor=0.6, align=True)
		row3s1.operator("sss.stitch", text='Stitch', icon='CURVE_DATA')
		row3s2 = row3s1.split(align=True)
		row3s2.operator("sss.apply_stitch", text='Apply')

		row4 = layout.row()
		row4.operator("sss.bevel_03", text='Bevel 0.3mm')
		row4.operator("sss.shrink_03", text='Shrink -0.3mm')

		row9 = layout.row(align=True)
		row9.operator("sss.overlock", text='Overlock 1', icon='RNA')
		row9.operator("sss.overlock2", text='Overlock 2', icon='RNA')

		row5 = layout.row()
		row5.operator("sss.draw_curve", icon='GREASEPENCIL')
		row5.operator("sss.quad_remesh", icon='MOD_REMESH')

		row8 = layout.row()
		row8.operator("sss.subdivision", icon='MOD_SUBSURF')
		row8.operator("sss.subdivision", icon='MOD_REMESH')


class SSS_PT_UV(bpy.types.Panel):
	bl_label = "Genshoe UV tools"
	bl_idname = "SSS_PT_UV"
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = 'UI'
	bl_category = 'Genshoe'

	def draw(self, context):
		layout = self.layout
		layout.operator("sss.uv_rectangle", text="Rectangle", icon = "UV_FACESEL")
		layout.operator("sss.uv_real_size", text="Real size", icon='FULLSCREEN_ENTER')

def register():
	bpy.utils.register_class(SSS_PT_MAIN)
	bpy.utils.register_class(SSS_PT_UV)

def unregister():
	bpy.utils.unregister_class(SSS_PT_MAIN)
	bpy.utils.unregister_class(SSS_PT_UV)


