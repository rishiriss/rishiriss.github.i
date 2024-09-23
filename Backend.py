from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load dataset
file_path = 'bosch_item_based_collaborative_filteringg.csv'
df = pd.read_csv(file_path)

# Normalize the features
df['Avg. Rating'] = (df['Avg. Rating'] - df['Avg. Rating'].min()) / (df['Avg. Rating'].max() - df['Avg. Rating'].min())

# Helper function to get product and recommendations
def get_product_info(product_id):
    product_info = df[df['Product ID'] == product_id]
    if not product_info.empty:
        product = product_info.iloc[0]
        recommended_products = df.sample(4)[['Product Name', 'Avg. Rating', 'Image URL']]  # Random sample for demo
        return {
            'Product Name': product['Product Name'],
            'Avg. Rating': product['Avg. Rating'],
            'Image URL': product['Image URL'],
            'recommended': recommended_products.to_dict(orient='records')
        }
    else:
        return None

# Home route (Landing Page)
@app.route('/')
def home():
    return render_template('index.html')

# Product Details Route
@app.route('/product', methods=['POST'])
def product_page():
    product_id = request.form.get('product_id')
    product_info = get_product_info(int(product_id))
    
    if product_info:
        return render_template('product.html', product=product_info)
    else:
        return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True)
