#!/usr/bin/env python
import pandas as pd
import joblib

# Загрузка модели, обученной на полном остеопорозном наборе (например, из wd_unique_bmd)
model = joblib.load("wd_unique_bmd/rf_model.joblib")  # или другой путь
trained_features = model.feature_names_in_

# Загрузка feature_table для артрита
arth = pd.read_csv("wd_calc_features_arth/feature_table.tsv", sep="\t", index_col=0).T
arth.index = arth.index.str.replace("_r1.fastq.gz", "", regex=False).str.replace(
    "_r1", "", regex=False
)

# Оставляем только признаки, использованные при обучении
arth_filt = arth[trained_features]
arth_norm = arth_filt.div(arth_filt.sum(axis=1), axis=0).fillna(0)

# Предсказание
preds = model.predict(arth_norm)
result = pd.DataFrame({"sample": arth_norm.index, "predicted": preds})
result.to_csv("predictions_arth.csv", index=False)
print("Predictions saved. Class distribution:\n", result["predicted"].value_counts())
