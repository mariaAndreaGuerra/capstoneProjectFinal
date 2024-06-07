import React, { useEffect, useState } from 'react';
import './App.css';
import { fetchOrders } from '../api';

const OrderList = () => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        fetchOrders()
            .then(data => setOrders(data))
            .catch(error => console.error('Error fetching orders:', error));
    }, []);

    return (
        <div className="card">
            <h2>Orders</h2>
            {orders.map(order => (
                <div key={order.id} className="card">
                    <h3>Order #{order.id}</h3>
                    <p>Status: {order.status}</p>
                </div>
            ))}
        </div>
    );
};

export default OrderList;
