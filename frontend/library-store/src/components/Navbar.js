import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, IconButton } from '@mui/material';
import { styled } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';

const StyledLink = styled(Link)({
  color: 'inherit',
  textDecoration: 'none',
});

function Navbar({ user, navItems }) {
  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Library Store
        </Typography>
        {navItems.map((item) => (
          <Button
            key={item.path}
            color="inherit"
            component={StyledLink}
            to={item.path}
            onClick={item.onClick}
            startIcon={item.icon}
          >
            {item.label}
          </Button>
        ))}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;