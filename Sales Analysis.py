#!/usr/bin/env python
# coding: utf-8

# In[77]:


import pandas as pd
import os 


# ## Task 1: Merging 12 months of sales data into a single file

# In[78]:


df = pd.read_csv("Sales Data/Sales_April_2019.csv")

files = [file for file in os.listdir("Sales Data")]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("Sales Data/"+file)
    all_months_data = pd.concat([all_months_data, df])
    
all_months_data.to_csv("all_data.csv", index = False)


# #### Read in updated dataframe

# In[79]:


all_data = pd.read_csv("all_data.csv")
all_data.head()


# ## Task 2: Clean up the Data!

# ####      Drop rows of NAN

# In[80]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()

all_data = all_data.dropna(how="all")
all_data.head()


# #### Find 'Or' and delete it

# In[81]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data.head()


# #### Augment data with addition columns

# In[82]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# #### Add Sales Column 

# In[83]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# In[84]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.sample(10)


# #### Add a city column

# In[85]:


def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: get_city(x)+ ', ' + get_state(x)) 
all_data.head()


# In[ ]:





# ## Question 1: What was the best month for sales?

# In[86]:


results = all_data.groupby('Month').sum()


# In[87]:


import matplotlib.pyplot as plt


# In[89]:


months = range(1,13)

plt.bar(months, results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month Number')
plt.title('Sales by Month')
plt.show

plt.savefig("monthlysale.png")


# ## Question 2: What U.S. City had the highest number of sales

# In[90]:


results = all_data.groupby('City').sum()

cities = [city for city, df in all_data.groupby('City')]

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City')
plt.title('Sales by City')
plt.show()
plt.savefig("citysales.png")


# ## Question 3: What time should we display advertisements to maximize likelihood of customer's buying product?

# In[91]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[92]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data.head()


# In[93]:


hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.ylabel('Number of Orders')
plt.xlabel('Hour')
plt.grid()
plt.title('Number of Order by Hour')
plt.show()
plt.savefig("hourlyorders.png")


# ##### answer: Sales peek at 11am and 7pm, meaning we should display ad between 10am - 11pm and 6pm - 7pm.

# ## Question 4: What products are most often sold together?

# In[94]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()
df.head()


# In[95]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
    
for key, value in count.most_common(10):
    print(key, value)

    
    
    
    
    
    
    
    


# #### answer: Top 3 products sold together: 1. iPhone and Lightning Cable 2. Google Phone and USB-C Cable 3. iPhone and Wired Headphones

# ## Question 5: What product sold the most?

# In[96]:


all_data.head()


# In[97]:


#Groups the products and sums the quantity ordered
product_group = all_data.groupby('Product')
quantity_ordered = product_group[['Quantity Ordered']].sum()

products = [product for product, df in product_group]
quantities = quantity_ordered['Quantity Ordered']

# Creates a Bar Chart
plt.bar(products, quantities)
plt.xticks(rotation='vertical', size=8)
plt.xlabel('Product')
plt.ylabel('Quantity Ordered')
plt.title('Quantity Ordered by Product')
plt.show()

plt.savefig("quantiyordered.png")


# In[98]:


prices = product_group[['Price Each']].mean()

# Creates X and y axis
fig, ax1 = plt.subplots()
ax1.bar(products, quantities, color='c', label='Quantity Ordered')
ax1.set_xlabel('Product')
ax1.set_ylabel('Quantity Ordered', color='c')
ax1.tick_params('y', colors='c')

# Creates a second y-axis for prices
ax2 = ax1.twinx()
ax2.plot(products, prices, 'm-', label='Price Each')
ax2.set_ylabel('Price Each', color='m')
ax2.tick_params('y', colors='m')

# Rotating the x-axis labels vertically
ax1.tick_params(axis='x', rotation=90)

# Adds title
plt.title('Quantity Ordered and Price Each by Product')


plt.show()
plt.savefig("quantityXprice.png")


# In[ ]:




