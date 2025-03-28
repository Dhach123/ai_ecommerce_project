import React from 'react';

const Header = () => {
  return (
    <header style={styles.header}>
      <h1 style={styles.title}>🛍️ FUNKU Online Store</h1>
    </header>
  );
};

const styles = {
  header: {
    background: 'linear-gradient(90deg, #ff007f, #ffcc00)',
    color: 'white',
    textAlign: 'center',
    padding: '15px 0',
    fontSize: '28px',
    fontWeight: 'bold',
    fontFamily: "'Comic Sans MS', cursive, sans-serif",
    borderBottom: '4px solid #ff007f',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.2)',
  },
  title: {
    margin: 0,
    letterSpacing: '3px',
    textTransform: 'uppercase',
    textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
  },
};

export default Header;
