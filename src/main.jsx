import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from 'styled-components'
import App from './App'

// Theme configuration
const theme = {
  colors: {
    primary: '#2E7D32',     // Green
    secondary: '#FFC107',   // Amber
    accent: '#8BC34A',      // Light Green
    text: {
      primary: '#212121',
      secondary: '#757575',
      light: '#FFFFFF'
    },
    background: {
      light: '#FFFFFF',
      dark: '#333333'
    }
  },
  fonts: {
    body: "'Inter', sans-serif",
    heading: "'Inter', sans-serif"
  },
  breakpoints: {
    mobile: '320px',
    tablet: '768px',
    desktop: '1024px',
    large: '1200px'
  },
  spacing: {
    xs: '0.25rem',    // 4px
    sm: '0.5rem',     // 8px
    md: '1rem',       // 16px
    lg: '2rem',       // 32px
    xl: '4rem'        // 64px
  }
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <App />
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
)
