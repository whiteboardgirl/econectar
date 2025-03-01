import styled from 'styled-components'

const AboutSection = styled.section`
  padding: 6rem 2rem;
  background-color: #f9f9f9;
`

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`

const SectionTitle = styled.h2`
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
  
  &:after {
    content: '';
    position: absolute;
    bottom: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background-color: #F1C40F;
  }
`

const ContentWrapper = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  
  @media (max-width: 968px) {
    grid-template-columns: 1fr;
  }
`

const ImageContainer = styled.div`
  img {
    width: 100%;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 968px) {
    grid-row: 1;
  }
`

const TextContent = styled.div`
  h3 {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: #333;
  }
  
  p {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #555;
    margin-bottom: 1.5rem;
  }
`

const Features = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 2rem;
`

const FeatureItem = styled.div`
  display: flex;
  align-items: flex-start;
  
  svg {
    margin-right: 1rem;
    min-width: 24px;
    margin-top: 5px;
  }
  
  div {
    h4 {
      font-size: 1.2rem;
      margin-bottom: 0.5rem;
      color: #333;
    }
    
    p {
      font-size: 1rem;
      margin-bottom: 0;
    }
  }
`

const About = () => {
  return (
    <AboutSection id="about">
      <Container>
        <SectionTitle>About Stingless Bees</SectionTitle>
        
        <ContentWrapper>
          <ImageContainer>
            <img src="/assets/images/about-bg.jpg" alt="Stingless bee on flower" />
          </ImageContainer>
          
          <TextContent>
            <h3>Nature's Tiny Pollinators</h3>
            <p>
              Stingless bees (Meliponini) are a diverse group of bees that, as the name suggests, 
              cannot sting. These remarkable creatures are found in tropical and subtropical regions 
              worldwide, with over 500 species identified so far.
            </p>
            <p>
              Unlike their more famous relatives, the honey bees, stingless bees have evolved 
              different defense mechanisms and social structures. They play a crucial role in 
              pollinating wild plants and crops, contributing significantly to biodiversity 
              and food security.
            </p>
            
            <Features>
              <FeatureItem>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="12" fill="#F1C40F" fillOpacity="0.2"/>
                  <path d="M8 12L11 15L16 9" stroke="#F1C40F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <div>
                  <h4>Ecological Impact</h4>
                  <p>Critical pollinators for many plant species in tropical ecosystems</p>
                </div>
              </FeatureItem>
              
              <FeatureItem>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="12" fill="#F1C40F" fillOpacity="0.2"/>
                  <path d="M8 12L11 15L16 9" stroke="#F1C40F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <div>
                  <h4>Medicinal Honey</h4>
                  <p>Produce honey with unique antibacterial properties</p>
                </div>
              </FeatureItem>
              
              <FeatureItem>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="12" fill="#F1C40F" fillOpacity="0.2"/>
                  <path d="M8 12L11 15L16 9" stroke="#F1C40F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <div>
                  <h4>Social Structure</h4>
                  <p>Live in complex colonies with specialized roles and communication</p>
                </div>
              </FeatureItem>
              
              <FeatureItem>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="12" fill="#F1C40F" fillOpacity="0.2"/>
                  <path d="M8 12L11 15L16 9" stroke="#F1C40F" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <div>
                  <h4>Threatened Species</h4>
                  <p>Many species face habitat loss and climate change challenges</p>
                </div>
              </FeatureItem>
            </Features>
          </TextContent>
        </ContentWrapper>
      </Container>
    </AboutSection>
  )
}

export default About
