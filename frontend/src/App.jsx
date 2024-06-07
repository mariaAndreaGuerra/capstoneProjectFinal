import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import ProductList from './components/ProductList';
import ProductForm from './components/ProductForm';
import OrderList from './components/OrderList';

const App = () => {
    return (
        <div>
            <Navbar />
            <div className="container">
                <ProductForm />
                <ProductList />
                <OrderList />
            </div>
        </div>
    );
};

export default App;
