# The code and dataset for the paper: Trajectory-based fish event classification through pre-training with diffusion models

## Highlights
- **Enhancing Fish Event Recognition:** We enhance the field of automatic fish event recognition in natural underwater videos, addressing the current gap in understanding fish interaction and competition, including predator-prey relationships and behaviors during mating seasons, particularly for male corkwing wrasse.

- **Novel Deep Learning Approach:** Our study makes a pioneering contribution to ecological informatics by introducing a novel deep learning approach to analyzing fish trajectories for behavior classification. This method utilizes unsupervised pre-training based on diffusion models to enhance feature learning.

- **Introducing a New Dataset:** We introduce a dataset of 16,937 trajectories across 12 event classes, benchmarked with several methods, confirming the superior performance of the proposed approach.

![GraphicalAbstract](https://github.com/NoeCanovi/Fish_Behaviors_Generative_Models/blob/main/graphicalAbstract.png)


## Project Structure

- **Data_cleaning Folder:** Contains the processes performed on the original datasets, not on the individual trajectories, whose lengths are fixed.
- **Models Folder:** Includes the `Autoencoder` and `Diffusion Model` Jupyter Notebook files.
  - The `Autoencoder` should work independently.
  - The `Diffusion Model` requires files from the `video_anomaly_diffusion-main` folder, which is a slightly modified version of [video_anomaly_diffusion](https://github.com/AnilOsmanTur/video_anomaly_diffusion).

**Note:** Paths need to be updated, as well as `wandb` project and entity names.


### If you use the code and/or the dataset, please cite:

```bibtex
@article{CANOVI2024102733,
  title        = {Trajectory-based fish event classification through pre-training with diffusion models},
  author       = {Noemi Canovi and Benjamin A. Ellis and Tonje K. Sørdalen and Vaneeda Allken and Kim T. Halvorsen and Ketil Malde and Cigdem Beyan},
  journal      = {Ecological Informatics},
  volume       = {82},
  pages        = {102733},
  year         = {2024},
  doi          = {10.1016/j.ecoinf.2024.102733},
  url          = {https://www.sciencedirect.com/science/article/pii/S1574954124002759},
}
