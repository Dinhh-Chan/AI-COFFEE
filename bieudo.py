import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc file Excel
df = pd.read_excel('dinhtran.xlsx')

# Chuyển đổi cột transaction_date thành kiểu datetime
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Tính doanh thu cho mỗi giao dịch
df['revenue'] = df['transaction_qty'] * df['unit_price']

# Tạo một cột mới chỉ chứa tháng và năm
df['month_year'] = df['transaction_date'].dt.to_period('M')

# Lọc và tính tổng doanh thu cho mỗi sản phẩm theo từng tháng
for month in df['month_year'].unique():
    # Tạo một DataFrame mới cho mỗi tháng
    month_data = df[df['month_year'] == month]
    revenue_per_product = month_data.groupby('product_detail')['revenue'].sum().reset_index()
    revenue_per_product = revenue_per_product.sort_values('revenue', ascending=False)
    
    # Vẽ biểu đồ cho mỗi tháng
    plt.figure(figsize=(10, 8))
    sns.barplot(x='revenue', y='product_detail', data=revenue_per_product)
    plt.title(f'Doanh thu theo từng sản phẩm cho {month}')
    plt.xlabel('Tổng doanh thu')
    plt.ylabel('Chi tiết sản phẩm')
    plt.show()
