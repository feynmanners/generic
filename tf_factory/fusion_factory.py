from neural_toolbox.fuse_mechanism import *

def get_fusion_mechanism(input1, input2, config, dropout_keep=1, reuse=False):

    assert len(input1.shape) == len(input2.shape) and len(input1.shape) == 2

    fusing_mode = config.get("mode", None)
    need_dropout = False

    if fusing_mode == "none":
        if input1 is None:
            fuse_out = input2
        elif input2 is None:
            fuse_out = input1
        else:
            assert False, "Could not use the fusing mode 'none' when both inputs are provided"

    elif fusing_mode == "concat":
        fuse_out = fuse_by_concat(input1, input2)

    elif fusing_mode == "dot":
        fuse_out = fuse_by_dot_product(input1, input2)

    elif fusing_mode == "full":
        fuse_out = fuse_by_brut_force(input1, input2)

    elif fusing_mode == "vis":
        fuse_out = fuse_by_vis(input1,input2,
                                projection_size=config['projection_size'],
                                apply_proj1=config.get('apply_proj1',True),
                                apply_proj2=config.get('apply_proj2', True),
                                output_size=config['output_size'],
                                dropout_keep=dropout_keep,
                                reuse=reuse)
        need_dropout = True
    else:
        assert False, "Invalid fusing mode '{}'".format(fusing_mode)

    return fuse_out, need_dropout