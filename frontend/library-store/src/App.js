import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import BookList from './components/BookList';
import HomeIcon from '@mui/icons-material/Home';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import LoginIcon from '@mui/icons-material/Login';
import LogoutIcon from '@mui/icons-material/Logout';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  const navItems = [
    { path: '/', label: 'Home', icon: <HomeIcon /> },
    { path: '/books', label: 'Books', icon: <MenuBookIcon /> },
    ...(user
      ? [{ path: '/logout', label: 'Logout', icon: <LogoutIcon />, onClick: handleLogout }]
      : [{ path: '/login', label: 'Login', icon: <LoginIcon /> }]),
  ];

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Navbar user={user} navItems={navItems} />
          <Routes>
            <Route path="/" element={<Home isLoggedIn={!!user} handleLogout={handleLogout}  />} />
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="/books" element={user ? <BookList access_token={user.access_token} /> : <Navigate to="/login" />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;