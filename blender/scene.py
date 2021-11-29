from os import remove
from os.path import dirname, exists

from ..imprt import preset_import

from .. import log, os as xm_os
logger = log.get_logger()


def save_blend(outpath=None, delete_overwritten=False):
    """Saves current scene to a .blend file.

    Args:
        outpath (str, optional): Path to save the scene to, e.g.,
            ``'~/foo.blend'``. ``None`` means saving to the current file.
        delete_overwritten (bool, optional): Whether to delete or keep
            as .blend1 the same-name file.

    Writes
        - A .blend file.
    """
    bpy = preset_import('bpy', assert_success=True)

    if outpath is not None:
        # "Save as" scenario: delete and then save
        xm_os.makedirs(dirname(outpath))
        if exists(outpath) and delete_overwritten:
            remove(outpath)

    try:
        # bpy.ops.file.autopack_toggle()
        bpy.ops.file.pack_all()
    except RuntimeError:
        logger.error("Failed to pack some files")

    if outpath is None:
        # "Save" scenario: save and then delete
        bpy.ops.wm.save_as_mainfile()
        outpath = bpy.context.blend_data.filepath
        bakpath = outpath + '1'
        if exists(bakpath) and delete_overwritten:
            remove(bakpath)
    else:
        bpy.ops.wm.save_as_mainfile(filepath=outpath)

    logger.info("Saved to %s", outpath)


def open_blend(inpath):
    """Opens a .blend file.

    Args:
        inpath (str): E.g., ``'~/foo.blend'``.
    """
    bpy = preset_import('bpy', assert_success=True)

    bpy.ops.wm.open_mainfile(filepath=inpath)

def add_environment_map(envmap_path):
    """Add environment map to world for more nature illumination"""
    bpy = preset_import('bpy', assert_success=True)
    nodes = bpy.context.scene.world.node_tree.nodes
    links = bpy.context.scene.world.node_tree.links
    env_texture_node = nodes.new(type="ShaderNodeTexEnvironment")
    env_texture_node.image = bpy.data.images.load(envmap_path)
    links.new(env_texture_node.outputs[0], nodes["World Output"].inputs[0])

def add_material(color, name=None):
    bpy = preset_import('bpy', assert_success=True)
    material = bpy.data.materials.new(name=f"material" if name is None else name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    principle_bsdf = nodes["Principled BSDF"]
    principle_bsdf.inputs[0].default_value = color
    return material
