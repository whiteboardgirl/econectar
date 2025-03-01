import { useState, useEffect } from 'react'
import styled from 'styled-components'

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s ease;
  z-index: 1000;
  background-color: ${({ scrolled }) => scrolled ? 'rgba(255, 255, 255, 0.95)' : 'transparent'};
  box-shadow: ${({ scrolled }) => scrolled ? '0 2px 10px rgba(0, 0, 0, 0.1)' : 'none'};
`

const Logo = styled.div`
  display: flex;
  align-items: center;
  
  img {
    height: 40px;
  }
  
  h1 {
    margin-left: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: ${({ scrolled }) => scrolled ? '#333' : '#fff'};
  }
`

const NavLinks = styled.nav`
  @media (max-width: 768px) {
    display: ${({ isOpen }) => isOpen ? 'flex' : 'none'};
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: white;
    padding: 1rem 0;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
    
    a {
      color: #333 !important;
      margin: 0.5rem 0;
    }
  }
  
  @media (min-width: 769px) {
    display: flex;
    gap: 2rem;
  }
  
  a {
    text-decoration: none;
    font-weight: 500;
    color: ${({ scrolled }) => scrolled ? '#333' : '#fff'};
    transition: color 0.3s ease;
    
    &:hover {
      color: #F1C40F;
    }
  }
`

const MenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: ${({ scrolled }) => scrolled ? '#333' : '#fff'};
  
  @media (max-width: 768px) {
    display: block;
  }
`

const Header = () => {
  const [scrolled, setScrolled] = useState(false)
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true)
      } else {
        setScrolled(false)
      }
    }
    
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])
  
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }
  
  return (
    <HeaderContainer scrolled={scrolled}>
      <Logo scrolled={scrolled}>
        <img src="/assets/icons/logo.svg" alt="EcoNectar Logo" />
        <h1>EcoNectar</h1>
      </Logo>
      
      <MenuButton scrolled={scrolled} onClick={toggleMenu}>
        ☰
      </MenuButton>
      
      <NavLinks scrolled={scrolled} isOpen={isMenuOpen}>
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#projects">Projects</a>
        <a href="#contact">Contact</a>
      </NavLinks>
    </HeaderContainer>
  )
}

export default Header
