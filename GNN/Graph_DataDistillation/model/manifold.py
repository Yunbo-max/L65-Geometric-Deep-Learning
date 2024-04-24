# -*- coding: utf-8 -*-
# @Author: Yunbo
# @Date:   2024-04-21 18:20:45
# @Last Modified by:   Yunbo
# @Last Modified time: 2024-04-21 18:23:46


import torch.nn as nn
import torch.nn.functional as F
import math
import torch
import torch.optim as optim
from torch.nn.parameter import Parameter
from torch.nn.modules.module import Module
from itertools import product
import numpy as np

class PGE(nn.Module):

    def __init__(self, nfeat, nnodes, nhid=128, nlayers=3, device=None, args=None):
        super(PGE, self).__init__()

    def forward(self, x, inference=False):


    @torch.no_grad()
    def inference(self, x):


    def reset_parameters(self):

