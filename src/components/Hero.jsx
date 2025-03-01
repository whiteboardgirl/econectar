import styled from 'styled-components'

const HeroSection = styled.section`
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/assets/images/hero-bg.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  padding: 0 2rem;
  position: relative;
`

const Title = styled.h1`
  font-size: 3.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`

const Subtitle = styled.h2`
  font-size: 1.5rem;
  margin-bottom: 2rem;
  font-weight: 400;
  max-width: 800px;
  
  @media (max-width: 768px) {
    font-size: 1.2rem;
  }
`

const Button = styled.a`
  display: inline-block;
  background-color: #F1C40F;
  color: #333;
  padding: 0.8rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  border-radius: 30px;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  
  &:hover {
    background-color: #E5B913;
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  }
  
  &:active {
    transform: translateY(-1px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
  }
`

const ScrollDown = styled.div`
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  animation: bounce 2s infinite;
  cursor: pointer;
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0) translateX(-50%);
    }
    40% {
      transform: translateY(-20px) translateX(-50%);
    }
    60% {
      transform: translateY(-10px) translateX(-50%);
    }
  }
`

const Hero = () => {
  const scrollToAbout = () => {
    document.getElementById('about').scrollIntoView({ behavior: 'smooth' })
  }
  
  return (
    <HeroSection id="home">
      <Title>Discover the World of Latinoamerican Stingless Bees</Title>
      <Subtitle>
        Join us in our mission to protect these remarkable pollinators and their vital contribution to biodiversity
      </Subtitle>
      <Button href="#about">Learn More</Button>
      
      <ScrollDown onClick={scrollToAbout}>
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 5V19M12 19L5 12M12 19L19 12" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </ScrollDown>
    </HeroSection>
  )
}

export default Hero
