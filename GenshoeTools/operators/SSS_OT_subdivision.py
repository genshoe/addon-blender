import bpy

class SSS_OT_subdivision(bpy.types.Operator):
    bl_idname = "sss.subdivision"
    bl_label = "Subdivision"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Subdivision fail")
            return {'CANCELLED'}

        # Thêm modifier Subdivision
        mod = obj.modifiers.new(name="Subdivision", type='SUBSURF')
        mod.levels = 2

        # Apply modifier
        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)

        self.report({'INFO'}, "OK")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SSS_OT_subdivision)

def unregister():
    bpy.utils.unregister_class(SSS_OT_subdivision)
