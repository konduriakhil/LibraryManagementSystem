import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { Link } from 'react-router-dom';

function Header({ isLoggedIn, darkMode, toggleTheme }) {
  return (
    <AppBar position="static">
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <img 
            src="https://d502jbuhuh9wk.cloudfront.net/logos/640864ece4b04cd73b1926a9.png" 
            alt="Learning Thoughts Library Logo" 
            style={{ height: '40px', marginRight: '10px' }}
          />
          <Typography variant="h6" component="div">
            Learning Thoughts Library
          </Typography>
        </Box>
        {isLoggedIn && (
          <>
            <Button color="inherit" component={Link} to="/books">Books</Button>
            <Button color="inherit" component={Link} to="/profile">Profile</Button>
          </>
        )}
        <IconButton color="inherit" onClick={toggleTheme}>
          {darkMode ? <Brightness7 /> : <Brightness4 />}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}

export default Header;