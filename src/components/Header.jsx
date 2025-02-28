import styled from 'styled-components';

const Nav = styled.nav`
  background: white;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

const NavContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.h1`
  color: #2E7D32;
`;

const NavLinks = styled.div`
  display: flex;
  gap: 2rem;

  a {
    color: #333;
    text-decoration: none;
    &:hover {
      color: #2E7D32;
    }
  }
`;

function Header() {
  return (
    <Nav>
      <NavContainer>
        <Logo>Econectar</Logo>
        <NavLinks>
          <a href="#about">About</a>
          <a href="#projects">Projects</a>
          <a href="#contact">Contact</a>
        </NavLinks>
      </NavContainer>
    </Nav>
  );
}

export default Header;
