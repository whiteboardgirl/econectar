import { styled } from 'styled-components'

const Container = styled.div`
  min-height: 100vh;
  background-color: #2E7D32;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
`

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: 1rem;
`

function App() {
  return (
    <Container>
      <Title>Econectar</Title>
    </Container>
  )
}

export default App
