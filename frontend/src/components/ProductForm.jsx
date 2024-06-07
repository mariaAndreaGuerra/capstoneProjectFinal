import React, { useState } from 'react';
import './App.css';
import { addProduct } from '../api';

const ProductForm = () => {
    const [product, setProduct] = useState({ name: '', description: '' });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProduct({ ...product, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        addProduct(product)
            .then(() => setProduct({ name: '', description: '' }))
            .catch(error => console.error('Error adding product:', error));
    };

    return (
        <div className="card">
            <h2>Add Product</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    value={product.name}
                    onChange={handleChange}
                    placeholder="Product Name"
                    required
                />
                <input
                    type="text"
                    name="description"
                    value={product.description}
                    onChange={handleChange}
                    placeholder="Product Description"
                    required
                />
                <button type="submit">Add Product</button>
            </form>
        </div>
    );
};

export default ProductForm;
