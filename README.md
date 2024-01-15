# Classifying Fish Behaviors through Trajectory-Based Generative Model Pretraining

This repository includes the code used in a master thesis regarding classifying Corwing Wrasse's behaviors with Autoencoder and Diffusion Model pretraining, plus a MLP for classification.

Data_cleaning folder includes the processes done on the original datasets.

Models folder include Autoencoder and Diffusion Model ipynb files. Autoencoder should work on its own. Diffusion Model requires files from video_anomaly_diffusion-main folder, a slightly modified version of [video_anomaly_diffusion](https://github.com/AnilOsmanTur/video_anomaly_diffusion/tree/main).

Note: paths need to be changed, as well as wandb project and entity names
