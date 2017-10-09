import tensorflow as tf

from neural_toolbox.cbn_pluggin import CBNfromLSTM
from neural_toolbox.resnet import create_resnet
from neural_toolbox.cbn import ConditionalBatchNorm

from generic.tf_factory.attention_factory import get_attention

def get_image_features(image, question, is_training, scope_name, dropout_keep, config):
    image_input_type = config["image_input"]

    # Extract feature from 1D-image feature s
    if image_input_type == "fc8" \
            or image_input_type == "fc7" \
            or image_input_type == "dummy":

        image_out = image
        if config.get('normalize', False):
            image_out = tf.nn.l2_normalize(image, dim=1, name="fc_normalization")

    elif image_input_type.startswith("conv") or image_input_type == "raw":

        # Extract feature from raw images
        if image_input_type == "raw":

            # Create CBN
            cbn = None
            if config["cbn"].get("use_cbn", False):
                cbn_factory = CBNfromLSTM(question, no_units=config['cbn']["cbn_embedding_size"])

                excluded_scopes = config["cbn"].get('excluded_scope_names', [])
                cbn = ConditionalBatchNorm(cbn_factory, excluded_scope_names=excluded_scopes,
                                           is_training=is_training)

            # Create ResNet
            resnet_version = config['resnet_version']
            image_feature_maps = create_resnet(image,
                                                 is_training=is_training,
                                                 scope=scope_name,
                                                 cbn=cbn,
                                                 resnet_version=resnet_version)

            image_feature_maps = image_feature_maps
            if config.get('normalize', False):
                image_feature_maps = tf.nn.l2_normalize(image_feature_maps, dim=[1, 2, 3])

        # Extract feature from 3D-image features
        else:
            image_feature_maps = image

        # apply attention
        image_out = get_attention(image_feature_maps, question, config["attention"], dropout_keep)

    else:
        assert False, "Wrong input type for image"

    return image_out
