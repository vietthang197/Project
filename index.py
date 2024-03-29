import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

print("1 \n")
print("Train data shape:", train.shape)
print("Test data shape:", test.shape)



print("2 \n")
print(train.head())
plt.style.use(style='ggplot')
plt.rcParams['figure.figsize'] = (10, 6)

print("3 \n")
print (train.SalePrice.describe())

print("5 \n")
target = np.log(train.SalePrice)
print ("\n Skew", target.skew())
plt.hist(target, color='blue')
plt.show()

print("6 \n")
numeric_features = train.select_dtypes(include=[np.number])
print(numeric_features.dtypes)

print("7 \n")
corr = numeric_features.corr()
print (corr['SalePrice'].sort_values(ascending=False)[:5], '\n')
print (corr['SalePrice'].sort_values(ascending=False)[-5:])

print("8 \n")
print(train.OverallQual.unique())

print("9 \n")
quality_pivot = train.pivot_table(index='OverallQual', values='SalePrice', aggfunc=np.median)
print(quality_pivot)

print("10 \n")
print("Show table")
quality_pivot.plot(kind='bar', color='blue')
plt.xlabel('Overall Quality')
plt.ylabel('Median Sale Price')
plt.xticks(rotation=0)
plt.show()

print("11 \n")
print("Show table")
plt.scatter(x=train['GrLivArea'], y=target)
plt.ylabel('Sale Price')
plt.xlabel('Grade (ground) living area')
plt.show()

print("12 \n")
print("Show table")
plt.scatter(x=train['GarageArea'], y=target)
plt.ylabel('Sale Price')
plt.xlabel('Garage Area')
plt.show()

print("13 \n")
print("Show table")
train = train[train['GarageArea'] < 1200]
plt.scatter(x=train['GarageArea'], y=np.log(train.SalePrice))
plt.xlim(-200,1600)
plt.ylabel('Sale Price')
plt.xlabel('Garage Area')
plt.show()

print("14 \n")
print("Show null count")
nulls = pd.DataFrame(train.isnull().sum().sort_values(ascending=False)[:25])
nulls.columns = ['Null Count']
nulls.index.name = 'Feature'
print(nulls)


print ("Unique values are:", train.MiscFeature.unique())

print("15 \n")
print("Data processing")
categoricals = train.select_dtypes(exclude=[np.number])
print(categoricals.describe())

print (train.Street.value_counts(), "\n")

train['enc_street'] = pd.get_dummies(train.Street, drop_first=True)
test['enc_street'] = pd.get_dummies(test.Street, drop_first=True)

print ('Encoded: \n')
print (train.enc_street.value_counts())


condition_pivot = train.pivot_table(index='SaleCondition', values='SalePrice', aggfunc=np.median)
condition_pivot.plot(kind='bar', color='blue')
plt.xlabel('Sale Condition')
plt.ylabel('Median Sale Price')
plt.xticks(rotation=0)
plt.show()
def encode(x): return 1 if x == 'Partial' else 0
train['enc_condition'] = train.SaleCondition.apply(encode)
test['enc_condition'] = test.SaleCondition.apply(encode)

condition_pivot = train.pivot_table(index='enc_condition', values='SalePrice', aggfunc=np.median)
condition_pivot.plot(kind='bar', color='blue')
plt.xlabel('Encoded Sale Condition')
plt.ylabel('Median Sale Price')
plt.xticks(rotation=0)
plt.show()
data = train.select_dtypes(include=[np.number]).interpolate().dropna()

print(sum(data.isnull().sum() != 0))

y = np.log(train.SalePrice)
X = data.drop(['SalePrice', 'Id'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=.33)

print("Linear Regression Model")
lr = linear_model.LinearRegression()
model = lr.fit(X_train, y_train)


print("R^2 is: \n", model.score(X_test, y_test))
predictions = model.predict(X_test)

print('RMSE is: \n', mean_squared_error(y_test, predictions))


actual_values = y_test
plt.scatter(predictions, actual_values, alpha=.75,
            color='b')
plt.xlabel('Predicted Price')
plt.ylabel('Actual Price')
plt.title('Linear Regression Model')
plt.show()


for i in range (-2, 3):
    alpha = 10**i
    rm = linear_model.Ridge(alpha=alpha)
    ridge_model = rm.fit(X_train, y_train)
    preds_ridge = ridge_model.predict(X_test)

    plt.scatter(preds_ridge, actual_values, alpha=.75, color='b')
    plt.xlabel('Predicted Price')
    plt.ylabel('Actual Price')
    plt.title('Ridge Regularization with alpha = {}'.format(alpha))
    overlay = 'R^2 is: {}\nRMSE is: {}'.format(
                    ridge_model.score(X_test, y_test),
                    mean_squared_error(y_test, preds_ridge))
    plt.annotate(s=overlay,xy=(12.1,10.6),size='x-large')
    plt.show()

print("R^2 is: \n", model.score(X_test, y_test))
submission = pd.DataFrame()
submission['Id'] = test.Id
feats = test.select_dtypes(
    include=[np.number]).drop(['Id'], axis=1).interpolate()
predictions = model.predict(feats)
final_predictions = np.exp(predictions)

print("Original predictions are: \n", predictions[:10], "\n")
print("Final predictions are: \n", final_predictions[:10])

submission['SalePrice'] = final_predictions
print(submission.head())
submission.to_csv('submission1.csv', index=False)

print("\n Finish")