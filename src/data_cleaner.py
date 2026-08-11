# src/data_cleaner.py
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer as SKKNNImputer  # Renamed to avoid conflicts

# ==========================================
# 1. MISSING VALUES IMPUTATION (Polymorphism)
# ==========================================

class BaseImputer(ABC):
    @abstractmethod
    def impute(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Abstract method to fill missing values in a specific column."""
        pass


class MeanImputer(BaseImputer):
    def impute(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Fills missing values with the mean of the column."""
        df_copy = df.copy()
        mean_value = df_copy[column].mean()
        df_copy[column] = df_copy[column].fillna(mean_value)
        return df_copy


class MedianImputer(BaseImputer):
    def impute(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Fills missing values with the median of the column."""
        df_copy = df.copy()
        median_value = df_copy[column].median()
        df_copy[column] = df_copy[column].fillna(median_value)
        return df_copy


class KNNImputer(BaseImputer):
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors

    def impute(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Fills missing values using the K-Nearest Neighbors algorithm."""
        df_copy = df.copy()
        
        # KNN requires numerical matrix. We isolate the target column and 
        # a helper numerical column (like popularity) to perform the neighbor search.
        # This keeps the logic simple for a 2nd-semester CS student.
        imputer = SKKNNImputer(n_neighbors=self.n_neighbors)
        
        # We find another numeric column that has no missing values to assist the imputer
        helper_col = 'popularity' if column != 'popularity' else 'duration_ms'
        
        subset = df_copy[[column, helper_col]].values
        imputed_subset = imputer.fit_transform(subset)
        
        # Extract the resolved target column
        df_copy[column] = imputed_subset[:, 0]
        return df_copy


# ==========================================
# 2. OUTLIER HANDLING (Polymorphism)
# ==========================================

class BaseOutlierHandler(ABC):
    @abstractmethod
    def handle(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Abstract method to handle outliers in a specific column."""
        pass


class IQROutlierHandler(BaseOutlierHandler):
    def handle(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Caps the outliers using the Interquartile Range (IQR) method."""
        df_copy = df.copy()
        
        Q1 = df_copy[column].quantile(0.25)
        Q3 = df_copy[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Capping outliers to bounds instead of dropping them (safer for dataset size)
        df_copy[column] = np.clip(df_copy[column], lower_bound, upper_bound)
        return df_copy


class ZScoreOutlierHandler(BaseOutlierHandler):
    def __init__(self, threshold=3.0):
        self.threshold = threshold

    def handle(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Caps the outliers using the Standard Score (Z-Score) method."""
        df_copy = df.copy()
        
        mean = df_copy[column].mean()
        std = df_copy[column].std()
        
        # Avoid division by zero if std is 0
        if std == 0:
            return df_copy
            
        # Standard formulation: Z = (X - mean) / std
        # We cap values where |Z| > threshold
        lower_bound = mean - self.threshold * std
        upper_bound = mean + self.threshold * std
        
        df_copy[column] = np.clip(df_copy[column], lower_bound, upper_bound)
        return df_copy
