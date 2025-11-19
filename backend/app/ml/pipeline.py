import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib, os

MODEL_DIR = '/data/models'
os.makedirs(MODEL_DIR, exist_ok=True)

def train_model(csv_path, target_col, model_type='decision_tree'):
    df = pd.read_csv(csv_path)
    if target_col not in df.columns:
        raise ValueError('target column not in CSV')
    y = df[target_col]
    X = df.drop(columns=[target_col])

    num_cols = X.select_dtypes(include=['number']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    preproc = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse=False), cat_cols)
    ], remainder='drop')

    if model_type == 'decision_tree':
        clf = DecisionTreeClassifier()
    elif model_type == 'random_forest':
        clf = RandomForestClassifier(n_estimators=100)
    elif model_type == 'logreg':
        clf = LogisticRegression(max_iter=1000)
    else:
        clf = DecisionTreeClassifier()

    pipe = Pipeline([('pre', preproc), ('clf', clf)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
        'recall': float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
        'f1': float(f1_score(y_test, y_pred, average='weighted', zero_division=0))
    }

    model_id = f"model_{int(pd.Timestamp.now().timestamp())}.joblib"
    model_path = os.path.join(MODEL_DIR, model_id)
    joblib.dump(pipe, model_path)

    return metrics, model_path

def infer_from_model(model_path, payload_rows):
    pipe = joblib.load(model_path)
    import pandas as pd
    df = pd.DataFrame(payload_rows)
    preds = pipe.predict(df)
    return preds.tolist()
