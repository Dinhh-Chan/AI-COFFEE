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
df['month'] = df['transaction_date'].dt.month

# Tạo một cột nhãn mới kết hợp product_id và product_detail
df['product_label'] = df['product_id'].astype(str) + " - " + df['product_detail']

# Tạo DataFrame mới tính tổng doanh thu cho mỗi sản phẩm theo từng tháng
revenue_per_product_per_month = df.groupby(['product_id', 'product_label', 'month'])['revenue'].sum().reset_index()

# Sắp xếp dữ liệu theo product_id và month
revenue_per_product_per_month.sort_values(['product_id', 'month'], inplace=True)

# Vẽ biểu đồ cột đứng cạnh nhau
plt.figure(figsize=(18, 10))
sns.barplot(x='product_label', y='revenue', hue='month', data=revenue_per_product_per_month, palette='viridis')
plt.title('So sánh doanh thu của các sản phẩm theo tháng')
plt.xlabel('Sản phẩm (ID - Chi tiết sản phẩm)')
plt.ylabel('Tổng doanh thu')
plt.xticks(rotation=90)  # Xoay nhãn trục x để dễ đọc hơn
plt.legend(title='Tháng')
plt.show()

# Tổng doanh thu của từng sản phẩm
total_revenue_per_product = df.groupby('product_detail')['revenue'].sum()

# Số lượng bán ra của từng sản phẩm
quantity_sold_per_product = df.groupby('product_detail')['transaction_qty'].sum()

# Tổng doanh thu và tổng số lượng bán ra
total_revenue = total_revenue_per_product.sum()
total_quantity_sold = quantity_sold_per_product.sum()

# Tính doanh thu trung bình và phần trăm đóng góp của từng sản phẩm
average_revenue_per_product = total_revenue_per_product / quantity_sold_per_product
contribution_percentage = (total_revenue_per_product / total_revenue) * 100

# Đánh giá toàn bộ sản phẩm
print("Đánh giá toàn bộ sản phẩm:")
print(f"Tổng doanh thu: {total_revenue}")
print(f"Tổng số lượng bán ra: {total_quantity_sold}")

# Đánh giá chi tiết từng sản phẩm
print("\nĐánh giá từng sản phẩm:")
detailed_evaluation = pd.DataFrame({
    'Tổng doanh thu': total_revenue_per_product,
    'Số lượng bán ra': quantity_sold_per_product,
    'Doanh thu trung bình': average_revenue_per_product,
    'Phần trăm đóng góp': contribution_percentage
})
doanhthu= detailed_evaluation.sort_values(by='Tổng doanh thu', ascending=False)
file_name = 'doanhthu.xlsx'

# Ghi biến 'doanhthu' vào file CSV
doanhthu.to_csv(file_name, index=False)
print(detailed_evaluation.sort_values(by='Tổng doanh thu', ascending=False))