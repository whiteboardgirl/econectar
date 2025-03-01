import styled from 'styled-components'

const Container = styled.div`
  min-height: 100vh;
  background-color: #2E7D32;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 20px;
`

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: 1rem;
`

const Subtitle = styled.p`
  font-size: 1.5rem;
  margin-bottom: 2rem;
  max-width: 600px;
`

const Button = styled.a`
  background-color: white;
  color: #2E7D32;
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
`

function App() {
  return (
    <Container>
      <Title>Econectar</Title>
      <Subtitle>
        Conectando pessoas e abelhas nativas através da meliponicultura sustentável
      </Subtitle>
      <Button href="#contact">Entre em Contato</Button>
    </Container>
  )
}

export default App
