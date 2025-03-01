import styled from 'styled-components'

const FooterContainer = styled.footer`
  background-color: #333;
  color: #fff;
  padding: 4rem 2rem 2rem;
`

const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  
  @media (max-width: 968px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: 576px) {
    grid-template-columns: 1fr;
  }
`

const FooterColumn = styled.div`
  h3 {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    color: #F1C40F;
    position: relative;
    
    &:after {
      content: '';
      position: absolute;
      bottom: -10px;
      left: 0;
      width: 40px;
      height: 2px;
      background-color: #F1C40F;
    }
  }
  
  p {
    margin-bottom: 1rem;
    line-height: 1.6;
    color: #ccc;
  }
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  li {
    margin-bottom: 0.8rem;
  }
  
  a {
    color: #ccc;
    text-decoration: none;
    transition: color 0.3s ease;
    display: inline-block;
    
    &:hover {
      color: #F1C40F;
    }
  }
`

const Newsletter = styled.form`
  display: flex;
  margin-top: 1rem;
  
  input {
    flex: 1;
    padding: 0.8rem;
    border: none;
    border-radius: 4px 0 0 4px;
    font-size: 0.9rem;
    
    &:focus {
      outline: none;
    }
  }
  
  button {
    background-color: #F1C40F;
    color: #333;
    border: none;
    padding: 0 1rem;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
    font-weight: 600;
    transition: background-color 0.3s ease;
    
    &:hover {
      background-color: #E5B913;
    }
  }
`

const FooterBottom = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 2rem;
  margin-top: 3rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  p {
    color: #aaa;
    font-size: 0.9rem;
  }
`

const SocialLinks = styled.div`
  display: flex;
  gap: 1rem;
  
  a {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.1);
    color: #fff;
    transition: all 0.3s ease;
    
    &:hover {
      background-color: #F1C40F;
      transform: translateY(-3px);
    }
  }
`

const Footer = () => {
  const handleNewsletterSubmit = (e) => {
    e.preventDefault()
    // Newsletter signup logic would go here
  }
  
  return (
    <FooterContainer>
      <FooterContent>
        <FooterColumn>
          <h3>About EcoNectar</h3>
          <p>
            EcoNectar is dedicated to the conservation of stingless bees through research, 
            education, and community initiatives. Our mission is to protect these vital 
            pollinators and promote sustainable practices.
          </p>
        </FooterColumn>
        
        <FooterColumn>
          <h3>Quick Links</h3>
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About Stingless Bees</a></li>
            <li><a href="#projects">Our Projects</a></li>
            <li><a href="#contact">Contact Us</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Resources</a></li>
          </ul>
        </FooterColumn>
        
        <FooterColumn>
          <h3>Our Projects</h3>
          <ul>
            <li><a href="#">Conservation Initiatives</a></li>
            <li><a href="#">Sustainable Meliponiculture</a></li>
            <li><a href="#">Research & Education</a></li>
            <li><a href="#">Community Outreach</a></li>
            <li><a href="#">Bee Rescue</a></li>
          </ul>
        </FooterColumn>
        
        <FooterColumn>
          <h3>Newsletter</h3>
          <p>Subscribe to our newsletter for updates on our projects and stingless bee news.</p>
          <Newsletter onSubmit={handleNewsletterSubmit}>
            <input type="email" placeholder="Your email address" required />
            <button type="submit">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </Newsletter>
        </FooterColumn>
      </FooterContent>
      
      <FooterBottom>
        <p>&copy; {new Date().getFullYear()} EcoNectar. All rights reserved.</p>
        
        <SocialLinks>
          <a href="#" aria-label="Facebook">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 2H15C13.6739 2 12.4021 2.52678 11.4645 3.46447C10.5268 4.40215 10 5.67392 10 7V10H7V14H10V22H14V14H17L18 10H14V7C14 6.73478 14.1054 6.48043 14.2929 6.29289C14.4804 6.10536 14.7348 6 15 6H18V2Z" fill="currentColor"/>
            </svg>
          </a>
          <a href="#" aria-label="Twitter">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M23 3C22.0424 3.67548 20.9821 4.19211 19.86 4.53C19.2577 3.83751 18.4573 3.34669 17.567 3.12393C16.6767 2.90116 15.7395 2.95721 14.8821 3.28444C14.0247 3.61167 13.2884 4.19439 12.773 4.9537C12.2575 5.71302 11.9877 6.61234 12 7.53V8.53C10.2426 8.57557 8.50127 8.18581 6.93101 7.39545C5.36074 6.60508 4.01032 5.43864 3 4C3 4 -1 13 8 17C5.94053 18.398 3.48716 19.0989 1 19C10 24 21 19 21 7.5C20.9991 7.22145 20.9723 6.94359 20.92 6.67C21.9406 5.66349 22.6608 4.39271 23 3V3Z" fill="currentColor"/>
            </svg>
          </a>
          <a href="#" aria-label="Instagram">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 2H7C4.23858 2 2 4.23858 2 7V17C2 19.7614 4.23858 22 7 22H17C19.7614 22 22 19.7614 22 17V7C22 4.23858 19.7614 2 17 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M16 11.37C16.1234 12.2022 15.9813 13.0522 15.5938 13.799C15.2063 14.5458 14.5932 15.1514 13.8416 15.5297C13.0901 15.9079 12.2385 16.0396 11.4078 15.9059C10.5771 15.7723 9.80977 15.3801 9.21485 14.7852C8.61993 14.1902 8.22774 13.4229 8.09408 12.5922C7.96042 11.7615 8.09208 10.9099 8.47034 10.1584C8.8486 9.40685 9.4542 8.79374 10.201 8.40624C10.9478 8.01874 11.7978 7.87659 12.63 8C13.4789 8.12588 14.2649 8.52146 14.8717 9.12831C15.4785 9.73515 15.8741 10.5211 16 11.37Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M17.5 6.5H17.51" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
          <a href="#" aria-label="LinkedIn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 8C17.5913 8 19.1174 8.63214 20.2426 9.75736C21.3679 10.8826 22 12.4087 22 14V21H18V14C18 13.4696 17.7893 12.9609 17.4142 12.5858C17.0391 12.2107 16.5304 12 16 12C15.4696 12 14.9609 12.2107 14.5858 12.5858C14.2107 12.9609 14 13.4696 14 14V21H10V14C10 12.4087 10.6321 10.8826 11.7574 9.75736C12.8826 8.63214 14.4087 8 16 8V8Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M6 9H2V21H6V9Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M4 6C5.10457 6 6 5.10457 6 4C6 2.89543 5.10457 2 4 2C2.89543 2 2 2.89543 2 4C2 5.10457 2.89543 6 4 6Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
        </SocialLinks>
      </FooterBottom>
    </FooterContainer>
  )
}

export default Footer
