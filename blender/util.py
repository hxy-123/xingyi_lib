from ..imprt import preset_import


def cursor_to(loc):
    """Moves the cursor to the given 3D location.

    Useful for inspecting where a 3D point is in the scene, to do which you
    first use this function, save the scene, and open the scene in GUI.

    Args:
        loc (array_like): 3D coordinates, of length 3.
    """
    bpy = preset_import('bpy', assert_success=True)

    bpy.context.scene.cursor.location = loc

def pose_cvt(T_cv):
    """
    Convert transformation from CV representation to Blender(opengl)
    Input: 4x4 Transformation matrix
    Output: 4x4 Converted transformation matrix
    """
    import numpy as np
    R = T_cv[:3, :3]
    t = T_cv[:3, 3]

    R_rot = np.eye(3)
    R_rot[1, 1] = -1
    R_rot[2, 2] = -1

    R = np.matmul(R_rot, R)
    t = np.matmul(R_rot, t)

    T_cg = np.eye(4)
    T_cg[:3, :3] = R
    T_cg[:3, 3] = t
    return T_cg
