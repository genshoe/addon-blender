from . import (
	SSS_OT_config_file,
	SSS_OT_stitch,
	SSS_OT_apply_stitch,
	SSS_OT_studio,
	SSS_OT_uv_real_size,
	SSS_OT_uv_to_mesh,
	SSS_OT_create_collection,
	SSS_OT_uv_remap_2d_to_3d,
	SSS_OT_apply_remap,
	SSS_OT_bake,
	SSS_OT_add_lattice,
	SSS_OT_apply_lattice,
	SSS_OT_set_origin_to_bottom,
	SSS_OT_edge_length,
	SSS_OT_bevel_03,
	SSS_OT_shrink_03,
	SSS_OT_draw_curve,
	SSS_OT_quad_remesh,
	SSS_OT_subdivision,
	SSS_OT_uv_rectangle,
	SSS_OT_overlock,
	SSS_OT_overlock2,
	SSS_OT_subdivision_toggle
)

classes = (
	SSS_OT_config_file,
	SSS_OT_stitch,
	SSS_OT_apply_stitch,
	SSS_OT_studio,
	SSS_OT_uv_real_size,
	SSS_OT_uv_to_mesh,
	SSS_OT_create_collection,
	SSS_OT_uv_remap_2d_to_3d,
	SSS_OT_apply_remap,
	SSS_OT_bake,
	SSS_OT_add_lattice,
	SSS_OT_apply_lattice,
	SSS_OT_set_origin_to_bottom,
	SSS_OT_edge_length,
	SSS_OT_bevel_03,
	SSS_OT_shrink_03,
	SSS_OT_draw_curve,
	SSS_OT_quad_remesh,
	SSS_OT_subdivision,
	SSS_OT_uv_rectangle,
	SSS_OT_overlock,
	SSS_OT_overlock2,
	SSS_OT_subdivision_toggle


)
def register():
	for cls in classes:
		cls.register()

def unregister():
	for cls in reversed(classes):
		cls.unregister()