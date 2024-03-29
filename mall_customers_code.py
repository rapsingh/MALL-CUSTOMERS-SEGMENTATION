# -*- coding: utf-8 -*-
"""mall_customers_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmGn35qE4aCAUDVPOwiFVZc2acF3v_M6

## Importing the libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

"""## Reading and analysing the data"""

df=pd.read_csv("Mall_Customers.csv")

df.head()

df.drop('CustomerID', axis=1, inplace=True)
print(df.head())

df.describe()

"""## Plotting various exploratory graphs to derive an understanding of the all customers"""

plt.figure(figsize=(10, 6))
sns.set(style = 'darkgrid')
sns.displot(df['Annual Income (k$)'])
plt.title('Distribution of Annual Income (k$)', fontsize = 20)
plt.xlabel('Range of Annual Income (k$)')
plt.ylabel('Count')

plt.figure(figsize=(10, 6))
sns.set(style = 'darkgrid')
sns.displot(df['Age'])
plt.title('Distribution of Age', fontsize = 20)
plt.xlabel('Range of Age')
plt.ylabel('Count')

plt.figure(figsize=(10, 6))
sns.set(style = 'darkgrid')
sns.displot(df['Spending Score (1-100)'])
plt.title('Distribution of Spending Score (1-100)', fontsize = 20)
plt.xlabel('Range of Spending Score (1-100)')
plt.ylabel('Count')

z = df.groupby(['Gender']).size().reset_index(name='count')
pieChart = px.pie(z, values='count', names='Gender', 
                  title='Distribution of Gender on dataset',
                  color_discrete_sequence=px.colors.qualitative.Set3)
pieChart.show()

fig = px.scatter_3d(df, x = 'Age', y='Annual Income (k$)', z='Spending Score (1-100)', color='Gender')
fig.show()

"""### We may be able to identify 5 clusters here

## Applying k-mean clustering
"""

X = df.iloc[:,2:4].values

ssd = []

K = range(1,15)
for k in K:
    kmean = KMeans(n_clusters=k, init='random', n_init=10, max_iter=500)
    kmean = kmean.fit(X)
    ssd.append(kmean.inertia_)

plt.plot(K, ssd, marker='o')
plt.xlabel('k')
plt.ylabel('ssd')
plt.show()

for n_cluster in range(2,15):
    kmeans = KMeans(n_clusters=n_cluster).fit(X)
    label = kmeans.labels_
    sil_coeff = silhouette_score(X, label, metric='euclidean')
    print("cluster={}, The silhouette Coeff = {}".format(n_cluster, sil_coeff))

kmeans = KMeans(n_clusters = 5, init="k-means++", max_iter = 500, n_init = 10)
clusters = kmeans.fit_predict(X)


finaldata = df.copy()
finaldata['Cluster'] = clusters
fig = px.scatter_3d(finaldata, x = 'Age', y='Annual Income (k$)', z='Spending Score (1-100)',
              color='Cluster', opacity = 0.8)
fig.show()

finaldata.head()