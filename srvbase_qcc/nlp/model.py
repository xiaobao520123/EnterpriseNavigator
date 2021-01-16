#!/usr/bin/env python36
# -*- coding: utf-8 -*-


import datetime
import math
import numpy as np
import torch
from torch import nn
from torch.nn import Module, Parameter
import torch.nn.functional as F


class Net(Module):
    def __init__(self, params):
        # todo 部署bert作为模型的输入
        super(Net, self).__init__()
        self.hidden_size = params['hidden_size']
        self.batch_size = params['batch_size']
        self.linear_one = nn.Linear(self.hidden_size, self.hidden_size, bias=True)
        self.linear_two = nn.Linear(self.hidden_size, self.hidden_size, bias=True)
        self.linear_three = nn.Linear(self.hidden_size, self.hidden_size, bias=True)
        self.linear_four = nn.Linear(self.hidden_size, 1, bias=False)
        self.linear_five = nn.Linear(self.hidden_size, 2, bias=False)
        self.loss_function = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.parameters(), lr=params['lr'], weight_decay=params['l2'])
        self.scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer, step_size=params['lr_dc_step'], gamma=params['lr_dc'])
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1.0 / math.sqrt(self.hidden_size)
        for weight in self.parameters():
            weight.data.uniform_(-stdv, stdv)

    def forward(self, hidden, mask):
        hidden = hidden * mask.unsqueeze(-1)
        ht = hidden[torch.arange(mask.shape[0]).long(), torch.sum(mask, 1) - 1]  # batch_size x latent_size
        q1 = self.linear_one(ht).view(ht.shape[0], 1, ht.shape[1])  # batch_size x 1 x latent_size
        q2 = self.linear_two(hidden)  # batch_size x seq_length x latent_size
        alpha = self.linear_four(torch.sigmoid(q1 + q2))
        hs = torch.sum(alpha * hidden * mask.view(mask.shape[0], -1, 1).float(), 1)
        h_last = self.linear_three(ht)
        representation = hs * h_last
        logits = self.linear_five(representation)
        # batch, 2

        return logits, representation









