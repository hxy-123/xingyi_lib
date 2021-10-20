import h5py
# h5py
def save_h5(dict_to_save, filename, transform_slash=True):
    """Saves dictionary to hdf5 file"""
    with h5py.File(filename, 'w') as f:
        for key in dict_to_save:  # h5py doesn't allow '/' in object name (will leads to sub-group)
            f.create_dataset(key.replace('/', '+') if transform_slash else key,
                             data=dict_to_save[key])


def load_h5(file_path, transform_slash=False):
    """load the whole h5 file into memory (not memmaped)
    """
    with h5py.File(file_path, 'r') as f:
        # if parallel:
        #     Parallel()
        data = {k if not transform_slash else k.replace('+', '/'): v.__array__() \
                    for k, v in f.items()}
    return data