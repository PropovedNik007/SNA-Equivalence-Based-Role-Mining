# Equivalence-Based Role Mining

This directory contains notebooks and tools which were used for completing Topic 4.

## Reproducibility steps

1. Create a virtual environment:
    `pip create -n venv venv`
    If you are using JupyterHub - skip this step.

2. Install required dependecies for correct work of notebooks:
    `pip install -r requirements.txt`
    If you are using JupyterHub - just type next string in any of notebooks:
    `!pip install -r requirements.txt`

3. Now everthing should work.

## Files Description

1. **post_to_post.py**: Role mining in post-to-post network.
    - This notebook contains code with preprocessing, creating post-to-post network and further fitting various role mining algorithms.

2. **role_mining.py**: General role mining notebook.
   - This notebook contains code with initial data investment, fitting to role mining pipeline and further analysis of article-postings-votes network.

3. **user_to_user.py** Role mining in user-to-user network. 
    - This notebook contains code with preprocessing, creating user-to-user network and further fitting various role mining algorithms.

4. **requirements.txt** Python requirements file.
    - This file contains the list of all required packages to run the code in three previous notebooks.

5. **utils/**
   - Folder containing helper files.
     1. **graphs.py**: Graph helper file.
        - This file contains functions which create diffrent network graphs.
     2. **methods.py**: Role miming pipeline.
        - This file contains functions for role mining and general pipeline for applying them sequentially and visualize results.
     3. **plots.py**: Plots helper file.
        - his file contains helper function for plotting graph.



