import bpy # type: ignore
import bmesh # type: ignore
from bpy.app.handlers import persistent # type: ignore

# tạo Property lưu tổng chiều dài
class SSS_OT_edge_length(bpy.types.PropertyGroup):
    edge_total_length_mm: bpy.props.FloatProperty(
        name = "Total length",
        default = 0,
    ) # type: ignore

# Tính tổng chiều dài
def get_selected_edge_length(context):
    obj = context.active_object
    if not obj or obj.mode != 'EDIT':
        return 0.0
    bm = bmesh.from_edit_mesh(obj.data)
    return sum(edge.calc_length() for edge in bm.edges if edge.select)

# Handler cập nhật chiều dài
@persistent
def update_edge_length(scene):
    if bpy.context.mode != 'EDIT_MESH':
        return

    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        total_length = get_selected_edge_length(bpy.context)
        scene.edge_length_props.edge_total_length_mm = total_length * 1000


def register():
    # Đăng ký class
    bpy.utils.register_class(SSS_OT_edge_length)

    # Đăng ký property
    # Tạo một property kiểu con trỏ (PointerProperty) trong Scene, trỏ tới một instance của class SSS_OT_edge_length.
    # Điều này giúp lưu trữ dữ liệu hoặc trạng thái liên quan đến class này trên Scene
    bpy.types.Scene.edge_length_props = bpy.props.PointerProperty(type=SSS_OT_edge_length)

    # Đăng ký Handler. sẽ chạy sau khi scene thay đổi
    # Gắn một callback function (update_edge_length) vào danh sách handler depsgraph_update_post
    bpy.app.handlers.depsgraph_update_post.append(update_edge_length)

def unregister():
    
    # gỡ bỏ handlers
    if update_edge_length in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(update_edge_length)

    # gỡ bỏ property
    del bpy.types.Scene.edge_length_props

    # gỡ bỏ class
    bpy.utils.unregister_class(SSS_OT_edge_length)
