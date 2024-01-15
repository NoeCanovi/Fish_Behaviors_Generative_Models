import math

import torch
from torch import nn
from torch.nn import functional as F
from torch import distributions

from .. import layers, utils


class GVADModel(nn.Module):
    def __init__(self,
                 feat_size,):
        super(GVADModel, self).__init__()
        self.ae = FeatureDenoiserModel(feat_size)


    def get_dis_thresh(self, dis_pred, th_alpha=0.1):
        d_std, d_mean = torch.std_mean(dis_pred, unbiased=True, dim=-1)
        return d_mean + th_alpha * d_std


    def loss(self, g_y, g_target):

        
        g_dist = (g_y - g_target).pow(2)
    
        g_loss = g_dist.mean(dim=1)
        
        return g_loss

    def forward(self, x_noised, sigma, cond=None):
        x_hat = self.ae(x_noised, sigma)
        return x_hat



class FiLM(nn.Module):
  """
  A Feature-wise Linear Modulation Layer from
  'FiLM: Visual Reasoning with a General Conditioning Layer'
  """
  def forward(self, x, gammas, betas):
      
    #gammas = gammas.unsqueeze(2).unsqueeze(3).expand_as(x)
    #gammas = gammas.unsqueeze(2).expand_as(x)
    #betas = betas.unsqueeze(2).expand_as(x)
    
    #print("gammas", gammas.size())
    #print("betas", betas.size())
    #print("x", x.size())
    #gammas = gammas.unsqueeze(1).expand_as(x)
    #betas = betas.unsqueeze(1).expand_as(x)
    gammas = gammas.unsqueeze(1)
    betas = betas.unsqueeze(1)

    
    #print("gammas", gammas.size())
    #print("gammas*x", (gammas*x).size())
    
    
    return (gammas * x) + betas
    
class FiLM1(nn.Module):
  """
  A Feature-wise Linear Modulation Layer from
  'FiLM: Visual Reasoning with a General Conditioning Layer'
  """
  def forward(self, x, gammas, betas):
      
    #gammas = gammas.unsqueeze(2).unsqueeze(3).expand_as(x)
    #gammas = gammas.unsqueeze(2).expand_as(x)
    #betas = betas.unsqueeze(2).expand_as(x)
    
    #print("gammas", gammas.size())
    #print("betas", betas.size())
    #print("x", x.size())
    #gammas = gammas.unsqueeze(1).expand_as(x)
    #betas = betas.unsqueeze(1).expand_as(x)
    gammas = gammas.unsqueeze(1)
    betas = betas.unsqueeze(1)
    x = x.unsqueeze(1)
    
    #print("gammas", gammas.size())
    #print("gammas*x", (gammas*x).size())
    
    
    return (gammas * x) + betas


def orthogonal_(module):
    nn.init.orthogonal_(module.weight)
    return module

class MappingNet(nn.Sequential):
    def __init__(self, feats_in, feats_out, n_layers=2):
        layers = []
        for i in range(n_layers):
            layers.append(orthogonal_(nn.Linear(feats_in if i == 0 else feats_out, feats_out)))
            layers.append(nn.GELU())
        super().__init__(*layers)
        

class FourierFeatures_aot(nn.Module):
    def __init__(self, in_features, out_features, std=1.):
        super().__init__()
        #assert out_features % 2 == 0
        self.register_buffer('weight', torch.randn([out_features, in_features]) * std)

    def forward(self, input):
        f = 2 * math.pi * input @ self.weight.T
        return f.cos(), f.sin()



'''   AutoEncoder Model   '''

# imports
from typing import List
import torch.nn as nn
import torch


# residual block for encoder
class ResConvBlock(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        bias: bool = True
    ) -> None:
        super(ResConvBlock, self).__init__()

        # 1d pooling with kernel = 2, it returns indices
        self.pool = nn.MaxPool1d(2, return_indices=True)
        self.relu = nn.ReLU(inplace=False)

        # encoder block
        self.block = nn.Sequential(
            nn.Conv1d(in_channels, out_channels, kernel_size=3, stride=1, bias=bias, padding = 1),
            nn.ReLU(inplace=False),
        )

        # convolutional layer shared by the residual block and the skip connection
        self.conv1 = self.block[0]

    def forward(self, x):
        identity = self.conv1(x)
        x = self.block(x)
        x = x + identity
        x = self.relu(x)
        return self.pool(x)


# residual block for decoder
class ResTConvBlock(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        bias: bool = True
    ) -> None:
        super(ResTConvBlock, self).__init__()
        self.relu = nn.ReLU(inplace=False)

        # batch normalization
        self.bn = nn.BatchNorm1d(out_channels)

        # decoder block
        self.block = nn.Sequential(
            nn.ConvTranspose1d(in_channels, out_channels, kernel_size=3, stride=1, bias=bias, padding=1),
            nn.ReLU(inplace=False),
        )

        # transpose layer shared by the skip and the decoder block
        self.devonc3 = self.block[0]

    def forward(self, x):
        identity = self.devonc3(x)
        x = self.block(x)
        x = x + identity
        x = self.relu(x)
        return self.bn(x)


class FeatureDenoiserModel(nn.Module):
    def __init__(
        self,
        layers: List[int] =  [64, 128],
        latent_space: int = 512,
        bias: bool = True
    ) -> None:
        super(FeatureDenoiserModel, self).__init__()
        self.layers = layers

        # definition encoder blocks
        self.enc_block1 = ResConvBlock(3, 64)
        self.enc_block2 = ResConvBlock(64, 128)

        # definition linear layer for the latent space
        self.encoder_fc = nn.Linear(128 * 3, 512, bias=bias)

        # definition decoder blocks
        self.dec_block2 = ResTConvBlock(128, 64)
        self.dec_block1 = ResTConvBlock(64, 3)

        # definition linear layer for the latent space
        self.decoder_fc = nn.Linear(512, 128 * 3, bias=bias)

        # definition batch norm for normalizing the latent space
        self.dec_bn = nn.BatchNorm1d(128)
        
        self.enc_tembed = FourierFeatures_aot(1, 13)
        self.dec_tembed = FourierFeatures_aot(1, 512)
        
        self.enc_in = FiLM()
        self.dec_in = FiLM1()
        

        self.initialize_weights()


    # initialize the weights
    def initialize_weights(self):
        for m in self.modules():
          if isinstance(m, nn.Conv1d) or isinstance(m, nn.ConvTranspose1d):
                nn.init.kaiming_normal_(m.weight,
                                        mode='fan_out',
                                        nonlinearity='relu')

          elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)


    # encoder function
    def encoder(self, x: torch.Tensor) -> torch.Tensor:
        x, self.i1 = self.enc_block1(x)
        x, self.i2 = self.enc_block2(x)
        x = self.encoder_fc(torch.flatten(x, 1))
        return x

    def freeze_encoder(self):
        self.enc_block1.requires_grad = False
        self.enc_block2.requires_grad = False
        self.encoder_fc.requires_grad = False
        print("Encoder is frozen")

    # decoder function
    def decoder(self, x: torch.Tensor) -> torch.Tensor:
        

        x = self.decoder_fc(x)
        
        x = self.dec_bn(x.view([-1, 128, 3]))
        

        self.unpool2 = torch.nn.MaxUnpool1d(2)
        x = self.unpool2(x, self.i2)
        
        x = self.dec_block2(x)
        

        self.unpool1 = torch.nn.MaxUnpool1d(2)
        x = self.unpool1(x, self.i1, output_size = [13])
        x = self.dec_block1(x)
        return x


    # forward function  
    def forward(self, x, sigma, model_cond=None):
        
        c_noise = sigma.log()/4

        enc_t = self.enc_tembed(utils.append_dims(c_noise, 2))
        dec_t = self.dec_tembed(utils.append_dims(c_noise, 2))
        
        x = self.enc_in(x, enc_t[0], enc_t[1])
        latent_code = self.encoder(x)
        
        #print("after enc", x.size())
        z = self.dec_in(latent_code, dec_t[0], dec_t[1])
        
        #print("after decin", z.size())
        z = self.decoder(z)
      
        return z
        
        
    def loss(self, g_y, g_target):
        
        g_dist = (g_y - g_target).pow(2)
        g_loss = g_dist.mean(dim=1)
        return g_loss


