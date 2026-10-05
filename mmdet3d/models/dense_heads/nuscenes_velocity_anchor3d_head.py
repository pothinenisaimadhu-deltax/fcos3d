# Copyright (c) OpenMMLab. All rights reserved.
"""A 9D Anchor3DHead variant for NuScenes velocity supervision.

The upstream Anchor3DHead uses 7D anchors.  NuScenes boxes add horizontal
velocity ``(vx, vy)``.  The existing DeltaXYZWLHRBBoxCoder and 3D IoU code
already support extra box dimensions, so this subclass only appends zero
velocity priors before target assignment and decoding.  This leaves the
standard Anchor3DHead unchanged for all existing models.
"""

from typing import List, Optional

import torch
from mmdet.models.utils import select_single_mlvl
from mmengine.config import ConfigDict

from mmdet3d.registry import MODELS
from .anchor3d_head import Anchor3DHead


@MODELS.register_module()
class NuScenesVelocityAnchor3DHead(Anchor3DHead):
    """Anchor3DHead with two learnable NuScenes velocity dimensions."""

    def get_anchors(self,
                    featmap_sizes: List[tuple],
                    input_metas: List[dict],
                    device: str = 'cuda') -> list:
        """Return 9D anchors by appending zero ``vx`` and ``vy`` priors."""
        anchor_list = super().get_anchors(featmap_sizes, input_metas, device)
        padded_anchor_list = []
        for multi_level_anchors in anchor_list:
            padded_levels = []
            for anchors in multi_level_anchors:
                if anchors.size(-1) != 7:
                    raise ValueError(
                        'NuScenesVelocityAnchor3DHead expects 7D geometric '
                        f'anchors, got {anchors.size(-1)} dimensions.')
                # Grid anchors retain spatial dimensions, e.g.
                # (z, y, x, rotations, box_dim); append velocity on box_dim.
                velocities = anchors.new_zeros((*anchors.shape[:-1], 2))
                padded_levels.append(torch.cat((anchors, velocities), dim=-1))
            padded_anchor_list.append(padded_levels)
        return padded_anchor_list

    def predict_by_feat(self,
                        cls_scores,
                        bbox_preds,
                        dir_cls_preds,
                        batch_input_metas=None,
                        cfg: Optional[ConfigDict] = None,
                        rescale: bool = False,
                        **kwargs):
        """Decode predictions with the same 9D priors used for training."""
        assert len(cls_scores) == len(bbox_preds) == len(dir_cls_preds)
        featmap_sizes = [score.shape[-2:] for score in cls_scores]
        priors = self.prior_generator.grid_anchors(
            featmap_sizes, device=cls_scores[0].device)
        mlvl_priors = []
        for prior in priors:
            prior = prior.reshape(-1, prior.size(-1))
            velocities = prior.new_zeros((prior.size(0), 2))
            mlvl_priors.append(torch.cat((prior, velocities), dim=-1))

        result_list = []
        for input_id in range(len(batch_input_metas)):
            result_list.append(self._predict_by_feat_single(
                cls_score_list=select_single_mlvl(cls_scores, input_id),
                bbox_pred_list=select_single_mlvl(bbox_preds, input_id),
                dir_cls_pred_list=select_single_mlvl(dir_cls_preds, input_id),
                mlvl_priors=mlvl_priors,
                input_meta=batch_input_metas[input_id],
                cfg=cfg,
                rescale=rescale,
                **kwargs))
        return result_list
