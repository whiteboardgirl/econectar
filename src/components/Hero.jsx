import styled from 'styled-components';

const HeroSection = styled.section`
  height: 100vh;
  background-image: linear-gradient(
    rgba(0, 0, 0, 0.5),
    rgba(0, 0, 0, 0.5)
  ), url('/assets/images/hero-bg.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
`;

const HeroContent = styled.div`
  max-width: 800px;
  padding: 0 20px;
`;

const Title = styled.h1`
  font-size: 3.5rem;
  margin-bottom: 1rem;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.5rem;
  margin-bottom: 2rem;
  
  @media (max-width: 768px) {
    font-size: 1.2rem;
  }
`;

const Button = styled.a`
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #2E7D32;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-size: 1.1rem;
  transition: background-color 0.3s;

  &:hover {
    background-color: #1B5E20;
  }
`;

function Hero() {
  return (
    <HeroSection>
      <HeroContent>
        <Title>Conectando Pessoas e Abelhas Nativas</Title>
        <Subtitle>
          Através da meliponicultura sustentável, preservamos a biodiversidade
          e promovemos o desenvolvimento local
        </Subtitle>
        <Button href="#about">Saiba Mais</Button>
      </HeroContent>
    </HeroSection>
  );
}

export default Hero;
