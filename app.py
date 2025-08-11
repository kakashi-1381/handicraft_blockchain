import hashlib
import json
import time
import qrcode
import streamlit as st

# Blockchain class to track products
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)
    
    def create_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def add_transaction(self, product_id, artisan_name, location, step_description, sustainability_details):
        self.current_transactions.append({
            'product_id': product_id,
            'artisan_name': artisan_name,
            'location': location,
            'timestamp': time.time(),
            'step_description': step_description,
            'sustainability_details': sustainability_details,
        })
        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]

# Function to generate QR codes for products
def generate_qr_code(product_id):
    # Create a local URL or replace with live URL
    blockchain_url = f"https://handicraftblockchain.streamlit.app/?product_id={product_id}"
    qr = qrcode.make(blockchain_url)
    qr.save(f"QR_{product_id}.png")

# Sample function to display product verification
def verify_product(product_id):
    # Simulate a product history from blockchain (this could be fetched from a real blockchain in the future)
    st.title(f"Product Verification for {product_id}")
    st.write(f"Product ID: {product_id}")
    st.write(f"Artisan: John Doe")
    st.write(f"Location: Village A")
    st.write(f"Step: Raw material sourcing")
    st.write(f"Sustainability: Organic cotton")
    
    # Add more fields as needed to display the product’s supply chain history

# Main app function
def app():
    # Capture product ID from the URL using `st.query_params()` (the new method)
    product_id = st.query_params.get("product_id", [None])[0]

    if product_id:
        verify_product(product_id)
    else:
        st.write("Please scan the QR code to verify the product.")

    # Input form to add product details
    st.title("Handicraft Blockchain Tracking System")
    product_id_input = st.text_input('Product ID')
    artisan_name = st.text_input('Artisan Name')
    location = st.text_input('Location')
    step_description = st.text_input('Step Description')
    sustainability_details = st.text_input('Sustainability Details')

    # Create a blockchain object
    blockchain = Blockchain()

    if st.button('Add Transaction'):
        blockchain.add_transaction(
            product_id_input,
            artisan_name,
            location,
            step_description,
            sustainability_details
        )
        blockchain.create_block(proof=blockchain.last_block['proof'])
        
        # Generate and display the QR code for the product
        generate_qr_code(product_id_input)
        st.image(f"QR_{product_id_input}.png", caption=f"QR Code for Product {product_id_input}")
        st.write(f"Transaction added for Product {product_id_input}")
        st.write(blockchain.chain)

if __name__ == "__main__":
    app()

