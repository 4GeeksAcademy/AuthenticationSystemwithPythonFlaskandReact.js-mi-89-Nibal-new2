import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Private = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      const token = sessionStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }
      try {
        const response = await fetch('/api/private', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        if (response.ok) {
          setUser(data.user);
        } else {
          setError(data.error || 'Failed to fetch user');
          sessionStorage.removeItem('token');
          navigate('/login');
        }
      } catch (err) {
        setError(err.message);
      }
    };
    fetchUser();
  }, [navigate]);

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="container">
      <h1>Private Dashboard</h1>
      {error && <p style={{color: 'red'}}>{error}</p>}
      {user && (
        <>
          <p>Welcome, {user.email}!</p>
          <button onClick={handleLogout}>Logout</button>
        </>
      )}
    </div>
  );
};

export default Private;
