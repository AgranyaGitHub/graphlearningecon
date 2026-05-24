from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

model = RandomForestClassifier()
model.fit(X_train, Y_train)
preds = model.predict(X_test)

print(classification_report(y_test, preds))