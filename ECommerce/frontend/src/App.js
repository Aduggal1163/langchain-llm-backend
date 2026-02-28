import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

// API Functions
const api = {
  // Users
  getUsers: () => axios.get(`${API_BASE}/users`),
  getUser: (id) => axios.get(`${API_BASE}/user/${id}`),
  createUser: (user) => axios.post(`${API_BASE}/users`, user),
  deleteUser: (id) => axios.delete(`${API_BASE}/users/${id}`),
  
  // Products
  getProducts: () => axios.get(`${API_BASE}/products`),
  getProduct: (id) => axios.get(`${API_BASE}/products/${id}`),
  createProduct: (product) => axios.post(`${API_BASE}/products`, product),
  deleteProduct: (id) => axios.delete(`${API_BASE}/products/${id}`),
  
  // Orders
  getOrders: () => axios.get(`${API_BASE}/orders`),
  getOrder: (id) => axios.get(`${API_BASE}/orders/${id}`),
  createOrder: (userId, order) => axios.post(`${API_BASE}/users/${userId}/orders`, order),
  updateOrderStatus: (id) => axios.put(`${API_BASE}/orders/${id}`),
};

// Styles
const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
  },
  navbar: {
    backgroundColor: '#2c3e50',
    padding: '1rem 2rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  navBrand: {
    color: 'white',
    fontSize: '1.5rem',
    fontWeight: 'bold',
    textDecoration: 'none',
  },
  navLinks: {
    display: 'flex',
    gap: '1rem',
  },
  navLink: {
    color: 'white',
    textDecoration: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    transition: 'background-color 0.3s',
  },
  navLinkActive: {
    backgroundColor: '#34495e',
  },
  main: {
    padding: '2rem',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  pageTitle: {
    fontSize: '2rem',
    marginBottom: '1.5rem',
    color: '#2c3e50',
  },
  card: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '1.5rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    marginBottom: '1.5rem',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  input: {
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
  },
  button: {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '1rem',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  buttonDanger: {
    backgroundColor: '#e74c3c',
  },
  buttonSuccess: {
    backgroundColor: '#27ae60',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  th: {
    textAlign: 'left',
    padding: '1rem',
    backgroundColor: '#f8f9fa',
    borderBottom: '2px solid #dee2e6',
  },
  td: {
    padding: '1rem',
    borderBottom: '1px solid #dee2e6',
  },
  status: {
    pending: {
      backgroundColor: '#ffc107',
      color: '#000',
      padding: '0.25rem 0.75rem',
      borderRadius: '4px',
      fontSize: '0.875rem',
    },
    completed: {
      backgroundColor: '#28a745',
      color: '#fff',
      padding: '0.25rem 0.75rem',
      borderRadius: '4px',
      fontSize: '0.875rem',
    },
  },
  emptyState: {
    textAlign: 'center',
    padding: '3rem',
    color: '#6c757d',
  },
  error: {
    backgroundColor: '#f8d7da',
    color: '#721c24',
    padding: '1rem',
    borderRadius: '4px',
    marginBottom: '1rem',
  },
  success: {
    backgroundColor: '#d4edda',
    color: '#155724',
    padding: '1rem',
    borderRadius: '4px',
    marginBottom: '1rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '1.5rem',
  },
  productCard: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '1.5rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  productName: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    marginBottom: '0.5rem',
  },
  productPrice: {
    fontSize: '1.5rem',
    color: '#27ae60',
    fontWeight: 'bold',
  },
  productStock: {
    color: '#6c757d',
    marginBottom: '1rem',
  },
  actions: {
    display: 'flex',
    gap: '0.5rem',
    marginTop: '1rem',
  },
};

// Navigation Component
function Navbar() {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path ? styles.navLinkActive : {};
  
  return (
    <nav style={styles.navbar}>
      <Link to="/" style={styles.navBrand}>🛒 ECommerce</Link>
      <div style={styles.navLinks}>
        <Link to="/" style={{...styles.navLink, ...isActive('/')}}>Products</Link>
        <Link to="/users" style={{...styles.navLink, ...isActive('/users')}}>Users</Link>
        <Link to="/orders" style={{...styles.navLink, ...isActive('/orders')}}>Orders</Link>
      </div>
    </nav>
  );
}

// Products Page
function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [newProduct, setNewProduct] = useState({ name: '', price: '', stock: '' });

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await api.getProducts();
      setProducts(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch products. Make sure the backend is running on localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createProduct({
        name: newProduct.name,
        price: parseFloat(newProduct.price),
        stock: parseInt(newProduct.stock)
      });
      setSuccess('Product created successfully!');
      setNewProduct({ name: '', price: '', stock: '' });
      setShowForm(false);
      fetchProducts();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to create product');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    try {
      await api.deleteProduct(id);
      setSuccess('Product deleted successfully!');
      fetchProducts();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to delete product');
    }
  };

  if (loading) return <div style={styles.main}>Loading...</div>;

  return (
    <div style={styles.main}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
        <h1 style={styles.pageTitle}>Products</h1>
        <button 
          style={styles.button} 
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Add Product'}
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}
      {success && <div style={styles.success}>{success}</div>}

      {showForm && (
        <div style={styles.card}>
          <h2 style={{marginBottom: '1rem'}}>Add New Product</h2>
          <form onSubmit={handleSubmit} style={styles.form}>
            <input
              style={styles.input}
              type="text"
              placeholder="Product Name"
              value={newProduct.name}
              onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
              required
            />
            <input
              style={styles.input}
              type="number"
              step="0.01"
              placeholder="Price"
              value={newProduct.price}
              onChange={(e) => setNewProduct({...newProduct, price: e.target.value})}
              required
            />
            <input
              style={styles.input}
              type="number"
              placeholder="Stock"
              value={newProduct.stock}
              onChange={(e) => setNewProduct({...newProduct, stock: e.target.value})}
              required
            />
            <button type="submit" style={styles.button}>Create Product</button>
          </form>
        </div>
      )}

      {products.length === 0 ? (
        <div style={styles.emptyState}>
          <p>No products found. Add your first product!</p>
        </div>
      ) : (
        <div style={styles.grid}>
          {products.map(product => (
            <div key={product.id} style={styles.productCard}>
              <div style={styles.productName}>{product.name}</div>
              <div style={styles.productPrice}>${product.price}</div>
              <div style={styles.productStock}>Stock: {product.stock}</div>
              <div style={styles.actions}>
                <button 
                  style={{...styles.button, ...styles.buttonDanger}}
                  onClick={() => handleDelete(product.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Users Page
function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [newUser, setNewUser] = useState({ username: '', email: '' });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await api.getUsers();
      setUsers(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch users. Make sure the backend is running on localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createUser({
        username: newUser.username,
        email: newUser.email
      });
      setSuccess('User created successfully!');
      setNewUser({ username: '', email: '' });
      setShowForm(false);
      fetchUsers();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to create user');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    try {
      await api.deleteUser(id);
      setSuccess('User deleted successfully!');
      fetchUsers();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to delete user');
    }
  };

  if (loading) return <div style={styles.main}>Loading...</div>;

  return (
    <div style={styles.main}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
        <h1 style={styles.pageTitle}>Users</h1>
        <button 
          style={styles.button} 
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Add User'}
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}
      {success && <div style={styles.success}>{success}</div>}

      {showForm && (
        <div style={styles.card}>
          <h2 style={{marginBottom: '1rem'}}>Add New User</h2>
          <form onSubmit={handleSubmit} style={styles.form}>
            <input
              style={styles.input}
              type="text"
              placeholder="Username"
              value={newUser.username}
              onChange={(e) => setNewUser({...newUser, username: e.target.value})}
              required
            />
            <input
              style={styles.input}
              type="email"
              placeholder="Email"
              value={newUser.email}
              onChange={(e) => setNewUser({...newUser, email: e.target.value})}
              required
            />
            <button type="submit" style={styles.button}>Create User</button>
          </form>
        </div>
      )}

      {users.length === 0 ? (
        <div style={styles.emptyState}>
          <p>No users found. Add your first user!</p>
        </div>
      ) : (
        <div style={styles.card}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Username</th>
                <th style={styles.th}>Email</th>
                <th style={styles.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td style={styles.td}>{user.id}</td>
                  <td style={styles.td}>{user.username}</td>
                  <td style={styles.td}>{user.email}</td>
                  <td style={styles.td}>
                    <button 
                      style={{...styles.button, ...styles.buttonDanger}}
                      onClick={() => handleDelete(user.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// Orders Page
function Orders() {
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [newOrder, setNewOrder] = useState({ userId: '', totalAmount: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [ordersRes, usersRes] = await Promise.all([
        api.getOrders(),
        api.getUsers()
      ]);
      setOrders(ordersRes.data);
      setUsers(usersRes.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch data. Make sure the backend is running on localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createOrder(parseInt(newOrder.userId), {
        total_amount: parseFloat(newOrder.totalAmount)
      });
      setSuccess('Order created successfully!');
      setNewOrder({ userId: '', totalAmount: '' });
      setShowForm(false);
      fetchData();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      const errorDetail = err.response?.data?.detail;
      if (Array.isArray(errorDetail)) {
        setError(errorDetail.map(e => e.msg).join(', '));
      } else {
        setError(errorDetail || 'Failed to create order');
      }
    }
  };

  const handleUpdateStatus = async (id) => {
    try {
      await api.updateOrderStatus(id);
      setSuccess('Order status updated to completed!');
      fetchData();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to update order status');
    }
  };

  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? user.username : `User #${userId}`;
  };

  if (loading) return <div style={styles.main}>Loading...</div>;

  return (
    <div style={styles.main}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
        <h1 style={styles.pageTitle}>Orders</h1>
        <button 
          style={styles.button} 
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Create Order'}
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}
      {success && <div style={styles.success}>{success}</div>}

      {showForm && (
        <div style={styles.card}>
          <h2 style={{marginBottom: '1rem'}}>Create New Order</h2>
          <form onSubmit={handleSubmit} style={styles.form}>
            <select
              style={styles.input}
              value={newOrder.userId}
              onChange={(e) => setNewOrder({...newOrder, userId: e.target.value})}
              required
            >
              <option value="">Select User</option>
              {users.map(user => (
                <option key={user.id} value={user.id}>{user.username} ({user.email})</option>
              ))}
            </select>
            <input
              style={styles.input}
              type="number"
              step="0.01"
              placeholder="Total Amount"
              value={newOrder.totalAmount}
              onChange={(e) => setNewOrder({...newOrder, totalAmount: e.target.value})}
              required
            />
            <button type="submit" style={styles.button}>Create Order</button>
          </form>
        </div>
      )}

      {orders.length === 0 ? (
        <div style={styles.emptyState}>
          <p>No orders found. Create your first order!</p>
        </div>
      ) : (
        <div style={styles.card}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Order ID</th>
                <th style={styles.th}>User</th>
                <th style={styles.th}>Total Amount</th>
                <th style={styles.th}>Status</th>
                <th style={styles.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td style={styles.td}>#{order.id}</td>
                  <td style={styles.td}>{getUserName(order.user_id)}</td>
                  <td style={styles.td}>${order.total_amount}</td>
                  <td style={styles.td}>
                    <span style={order.status === 'completed' ? styles.status.completed : styles.status.pending}>
                      {order.status}
                    </span>
                  </td>
                  <td style={styles.td}>
                    {order.status !== 'completed' && (
                      <button 
                        style={{...styles.button, ...styles.buttonSuccess}}
                        onClick={() => handleUpdateStatus(order.id)}
                      >
                        Mark Complete
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// Main App
function App() {
  return (
    <Router>
      <div style={styles.container}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Products />} />
          <Route path="/users" element={<Users />} />
          <Route path="/orders" element={<Orders />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
