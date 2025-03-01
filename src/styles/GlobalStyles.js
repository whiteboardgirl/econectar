import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  /* Reset CSS */
  *, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  /* Base HTML elements */
  html {
    font-size: 16px;
    scroll-behavior: smooth;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    font-family: ${props => props.theme.fonts.body};
    line-height: 1.5;
    color: ${props => props.theme.colors.text.primary};
    background-color: ${props => props.theme.colors.background.light};
    overflow-x: hidden;
  }

  /* Typography */
  h1, h2, h3, h4, h5, h6 {
    font-family: ${props => props.theme.fonts.heading};
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: ${props => props.theme.spacing.md};
  }

  h1 {
    font-size: 2.5rem;
    @media (min-width: ${props => props.theme.breakpoints.tablet}) {
      font-size: 3.5rem;
    }
  }

  h2 {
    font-size: 2rem;
    @media (min-width: ${props => props.theme.breakpoints.tablet}) {
      font-size: 2.5rem;
    }
  }

  h3 {
    font-size: 1.75rem;
  }

  p {
    margin-bottom: ${props => props.theme.spacing.md};
  }

  /* Links */
  a {
    color: ${props => props.theme.colors.primary};
    text-decoration: none;
    transition: color 0.3s ease;

    &:hover {
      color: ${props => props.theme.colors.accent};
    }
  }

  /* Images */
  img {
    max-width: 100%;
    height: auto;
    display: block;
  }

  /* Buttons */
  button {
    cursor: pointer;
    border: none;
    background: none;
    font-family: inherit;
    font-size: inherit;
    color: inherit;
    
    &:disabled {
      cursor: not-allowed;
      opacity: 0.7;
    }
  }

  /* Lists */
  ul, ol {
    margin-bottom: ${props => props.theme.spacing.md};
    padding-left: ${props => props.theme.spacing.lg};
  }

  /* Section spacing */
  section {
    padding: ${props => props.theme.spacing.xl} 0;
  }

  /* Container */
  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 ${props => props.theme.spacing.md};
  }

  /* Utility classes */
  .text-center {
    text-align: center;
  }

  .hidden {
    display: none;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* Animations */
  .fade-in {
    opacity: 0;
    animation: fadeIn 0.5s ease forwards;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Form elements */
  input,
  textarea,
  select {
    font-family: inherit;
    font-size: 1rem;
    padding: ${props => props.theme.spacing.sm};
    border: 1px solid ${props => props.theme.colors.text.secondary};
    border-radius: 4px;
    width: 100%;
    
    &:focus {
      outline: none;
      border-color: ${props => props.theme.colors.primary};
    }
  }

  /* Scrollbar styling */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: ${props => props.theme.colors.background.light};
  }

  ::-webkit-scrollbar-thumb {
    background: ${props => props.theme.colors.primary};
    border-radius: 4px;
  }

  /* Selection styling */
  ::selection {
    background: ${props => props.theme.colors.primary};
    color: white;
  }
`;

export default GlobalStyles;
