import React from 'react'
import styled from 'styled-components'

const Nav = styled.nav`
  padding: 1rem;
  background: white;
`

function Header() {
  return (
    <Nav>
      <h1>Econectar</h1>
    </Nav>
  )
}

export default Header
