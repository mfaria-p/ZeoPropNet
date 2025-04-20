# **ZeoPropNet: A Machine Learning Framework for Zeolite Property Prediction**

## 📌 **Overview**
ZeoPropNet is a **machine learning framework** designed for predicting various **zeolite properties**, particularly the framework density, using **neural networks**.This project was developed as part of a **student internship at Laboratório Associado LSRE-LCM (Porto, Portugal)** during July–August 2024. 

Built with **TensorFlow** and **Keras**, it supports:
- Cross-validation for robust model evaluation
- Hyperparameter tuning with **Keras Tuner**
- Model training and evaluation with automated scripts
- Configuration-driven experimentation for flexible model adjustments

📖 You can check the full project report and documentation [here](https://github.com/mfaria-p/ZeoPropNet/blob/d9cd6e0cb622776161c5900c0c5d68eb393c8e55/Final_report.pdf).

The datasets used were sourced from my [Web Scraping project](https://github.com/mfaria-p/Webscrapping_zeolites.git), which compiled zeolite data from the [International Zeolite Association (IZA)](https://www.iza-structure.org/databases/). By extracting **composite building units**, I generated **fingerprints** as input for the neural network.

---

## 🚀 **Key Features**
- **Cross-Validation**: Ensures robust model evaluation.
- **Hyperparameter Tuning**: Uses **Keras Tuner** for model optimization.
- **Model Training and Evaluation**: Provides automated scripts for training, testing, and evaluating models.
- **Configuration-Driven Approach**: Enables easy modification of model architecture and training parameters through config files.

---

## 📁 **Directory Structure**
```
MatPropNet/
|├── config_files/       # Configuration files for different models and datasets
|├── data/              # Datasets used for training and testing
|├── hyperband/         # Results from hyperparameter tuning
|├── main/              # Scripts for training, testing, and evaluation
|   |├── data.py            # Functions for data loading and preprocessing
|   |├── main_cv.py         # Script for cross-validation
|   |├── main_hyper.py      # Script for hyperparameter tuning
|   |├── model.py           # Functions for building and training models
|   |├── saving.py          # Functions for saving model history
|   └── stats.py           # Utility functions for statistical analysis
|└── models/            # Saved models and associated metadata
```

---

## ⚡ **Getting Started**

### **1. Install Dependencies**
Ensure **TensorFlow**, **Keras**, and other required libraries are installed.

### **2. Prepare Data**
Select the property to predict and the corresponding dataset in **data/**. The datasets contain **fingerprints** generated from **zeolite composite building units**.

### **3. Configure Models**
Modify the config files in **config_files/** to adjust model architecture and training parameters.

### **4. Run Scripts**
Execute scripts from **main/** to train, evaluate, and fine-tune models.

---

## 💻 **Example Usage**

### **Run Cross-Validation:**
```bash
python3 main/main_cv.py config_files/density_iza.cfg
```

### **Perform Hyperparameter Tuning:**
```bash
python3 main/main_hyper.py config_files/density_iza.cfg
```

---

## ✅ **Conclusion**
This project provides a structured framework for **zeolite property prediction** using machine learning, enabling efficient model training and evaluation.

```bash
python3 main/main_hyper.py config_files/density_iza.cfg
```



