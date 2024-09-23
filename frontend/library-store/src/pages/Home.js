import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Typography, Button, Box, Paper } from '@mui/material';

function Home({ isLoggedIn, handleLogout, token }) {
  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ width: '100%', mb: 4, overflow: 'hidden' }}>
          <Box
            sx={{
              height: 300,
              backgroundImage: 'url("https://thumbs.dreamstime.com/b/old-book-flying-letters-magic-light-background-bookshelf-library-ancient-books-as-symbol-knowledge-history-218640948.jpg")',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              display: 'flex',
              alignItems: 'flex-end',
              justifyContent: 'center',
              p: 4,
            }}
          >
            <Typography variant="h3" component="h1" sx={{ color: 'white', textShadow: '2px 2px 4px rgba(0,0,0,0.5)' }}>
              Learning Thoughts Library
            </Typography>
          </Box>
          <Box sx={{ p: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Welcome to our digital haven of knowledge
            </Typography>
            <Typography variant="body1" paragraph>
              Explore our vast collection of books, from classic literature to cutting-edge research. 
              Our library is designed to inspire, educate, and entertain readers of all ages and interests.
            </Typography>
            {isLoggedIn ? (
              <Box>
                <Typography variant="body1" gutterBottom>
                  Browse our collection of books and manage your account.
                </Typography>
                <Button variant="contained" onClick={handleLogout} sx={{ mt: 2 }}>Logout</Button>
              </Box>
            ) : (
              <Box>
                <Typography variant="body1" gutterBottom>
                  Please log in to access your account and start your reading journey.
                </Typography>
                <Button variant="contained" component={Link} to="/login" sx={{ mt: 2 }}>Login</Button>
              </Box>
            )}
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default Home;