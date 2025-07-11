bl_info = {
	"name": "1st Genshoe tools",
	"description": "Optimize workflow",
    "version": (1, 0, 0),
    "blender": (4, 3, 2),
    "location": "View3D > Sidebar > Genshoe",
	"category": "3D View",
    "doc_url": "https://sites.google.com/view/genshoe"
}

import importlib

from . import operators, panels

modules = [operators, panels]

def register():
    for m in modules:
        importlib.reload(m)
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()
