import styled from 'styled-components'

const HeroSection = styled.section`
  height: 90vh;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
              url('/images/hero-bg.jpg') center/cover;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
`

const Content = styled.div`
  max-width: 800px;
  padding: 0 20px;
`

const Title = styled.h1`
  font-size: 3.5rem;
  margin-bottom: 1rem;
`

const Subtitle = styled.p`
  font-size: 1.5rem;
  margin-bottom: 2rem;
`

const Button = styled.a`
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #2E7D32;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  transition: background-color 0.3s;

  &:hover {
    background-color: #1B5E20;
  }
`

function Hero() {
  return (
    <HeroSection>
      <Content>
        <Title>Conectando Pessoas e Abelhas Nativas</Title>
        <Subtitle>
          Através da meliponicultura sustentável, preservamos a biodiversidade
          e promovemos o desenvolvimento local
        </Subtitle>
        <Button href="#about">Saiba Mais</Button>
      </Content>
    </HeroSection>
  )
}

export default Hero
