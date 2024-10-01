import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
customers = pd.read_csv('../data/customers_dataset.csv')
geolocation = pd.read_csv('../data/geolocation_dataset.csv')
order_items = pd.read_csv('../data/order_items_dataset.csv')
order_payments = pd.read_csv('../data/order_payments_dataset.csv')
order_reviews = pd.read_csv('../data/order_reviews_dataset.csv')
orders = pd.read_csv('../data/orders_dataset.csv')
product_category_translation = pd.read_csv('../data/product_category_name_translation.csv')
products = pd.read_csv('../data/products_dataset.csv')
sellers = pd.read_csv('../data/sellers_dataset.csv')

# Title of the dashboard
st.title('E-Commerce Dashboard')

# Create a sidebar for navigation
st.sidebar.header('Navigation')
options = st.sidebar.selectbox('Select an option:', 
                                 ['Overview', 'Customer Analysis', 'Order Analysis', 'Product Analysis'])


# Function to create cards
def create_card(label, value, color):
    # Set the background color
    card_style = f"""
    <div style="background-color: {color}; border-radius: 10px; padding: 20px; text-align: center;">
        <h4 style="margin: 0; font-size: 25px; color: white;">{label}</h4>
        <h2 style="margin: 0; font-size: 32px; color: white;">{value}</h2>
    </div>
    """
    st.markdown(card_style, unsafe_allow_html=True)

# Overview Section
if options == 'Overview':
    st.header('Overview')
    
    # Total number of customers
    total_customers = customers['customer_unique_id'].nunique()

    # Total orders
    total_orders = orders['order_id'].nunique()

    # Total Products
    total_products = products['product_id'].nunique()

    # Create columns
    col1, col2, col3, col4 = st.columns(4)

    # Create cards for metrics in columns
    with col1:
        create_card('Total Customers', total_customers, '#4CAF50')  # Green

    with col2:
        create_card('Total Orders', total_orders, '#2196F3')         # Blue

    with col3:
        create_card('Total Products', total_products, '#FF9800')     # Orange

        

    # Add space between cards and charts
    st.write('')  # This creates a small space


    # Additional Visualizations
    st.subheader('Total Sales by Product Category')
    sales_per_category = order_items.merge(products, on='product_id')
    sales_summary = sales_per_category.groupby('product_category_name')['price'].sum().reset_index()
    sales_summary = sales_summary.sort_values(by='price', ascending=False).head(10)

    # Create a bar chart for the total sales by category
    fig, ax = plt.subplots()
    sns.barplot(data=sales_summary, x='price', y='product_category_name', ax=ax, palette='viridis')
    ax.set_title('Total Sales by Product Category')
    ax.set_xlabel('Total Sales (in currency)')
    ax.set_ylabel('Product Category')
    
    st.pyplot(fig)

    # Average Rating from Reviews
    st.subheader('Average Ratings from Reviews')
    # Ensure review ratings are numeric
    order_reviews['review_score'] = pd.to_numeric(order_reviews['review_score'], errors='coerce')
    average_rating = order_reviews['review_score'].mean()

    with col4:
        create_card('Average Review Score', round(average_rating, 2), '#FF5722')  # Red


    # Distribution of Ratings
    rating_counts = order_reviews['review_score'].value_counts().sort_index()

    # Create a bar chart for rating distribution
    fig2, ax2 = plt.subplots()
    sns.barplot(x=rating_counts.index, y=rating_counts.values, ax=ax2, palette='Blues')
    ax2.set_title('Distribution of Review Scores')
    ax2.set_xlabel('Review Score')
    ax2.set_ylabel('Number of Reviews')
    
    st.pyplot(fig2)

    # Show first few rows of orders dataset
    st.subheader('Sample Orders Data')
    st.write(orders.head())

# Customer Analysis Section
elif options == 'Customer Analysis':
    st.header('Customer Analysis')
    
    # Displaying customer counts by state
    customer_counts = customers['customer_state'].value_counts()
    st.bar_chart(customer_counts)

    # Show a table of customers
    st.subheader('Customer Data Sample')
    st.write(customers.head())


# Order Analysis Section
if options == 'Order Analysis':
    st.header('Order Analysis')

    # Ensure relevant columns are in datetime format
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

    # Calculate delivery time
    orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days

    # Display average delivery time
    average_delivery_time = orders['delivery_time'].mean()
    st.metric(label='Average Delivery Time (days)', value=average_delivery_time)

    # Plotting
    st.subheader('Delivery Time Distribution')
    st.bar_chart(orders['delivery_time'].value_counts())


## Product Analysis Section
elif options == 'Product Analysis':
    st.header('Product Analysis')
    
    # Get the most sold products
    sold_product_ids = order_items['product_id'].value_counts().head(10).index
    sold_product_counts = order_items['product_id'].value_counts().head(10).values

    # Map product IDs to product names
    product_names = products.set_index('product_id')['product_category_name']
    sold_product_names = product_names.loc[sold_product_ids]

    # Create a DataFrame for better visualization
    sold_products_df = pd.DataFrame({
        'Product Name': sold_product_names.values,
        'Sold Count': sold_product_counts
    })

    # Plotting the most sold products
    st.bar_chart(sold_products_df.set_index('Product Name'))

    # Show product data sample
    st.subheader('Product Data Sample')
    st.write(products.head())

st.caption('Copyright © Steven 2024')
