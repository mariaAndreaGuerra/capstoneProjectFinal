import React, { useEffect, useState } from 'react';
import './App.css';
import { fetchProducts } from '../api';

const ProductList = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetchProducts()
            .then(data => setProducts(data))
            .catch(error => console.error('Error fetching products:', error));
    }, []);

    return (
        <div className="card">
            <h2>Products</h2>
            {products.map(product => (
                <div key={product.id} className="card">
                    <h3>{product.name}</h3>
                    <p>{product.description}</p>
                </div>
            ))}
        </div>
    );
};

export default ProductList;
