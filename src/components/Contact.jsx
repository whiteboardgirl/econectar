import { useState } from 'react'
import styled from 'styled-components'

const ContactSection = styled.section`
  padding: 6rem 2rem;
  background-color: #f9f9f9;
`

const Container = styled.div`
  max-width: 1000px;
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

const ContactGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`

const ContactInfo = styled.div`
  h3 {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: #333;
  }
  
  p {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #555;
    margin-bottom: 2rem;
  }
`

const InfoItem = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  
  svg {
    min-width: 24px;
    margin-right: 1rem;
    color: #F1C40F;
  }
  
  span {
    font-size: 1.1rem;
    color: #555;
  }
`

const SocialLinks = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  
  a {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #F1C40F;
    color: white;
    transition: transform 0.3s ease, background-color 0.3s ease;
    
    &:hover {
      transform: translateY(-5px);
      background-color: #E5B913;
    }
  }
`

const ContactForm = styled.form`
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
`

const FormGroup = styled.div`
  margin-bottom: 1.5rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
  }
  
  input, textarea {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    
    &:focus {
      outline: none;
      border-color: #F1C40F;
    }
  }
  
  textarea {
    min-height: 150px;
    resize: vertical;
  }
`

const SubmitButton = styled.button`
  background-color: #F1C40F;
  color: #333;
  border: none;
  padding: 0.8rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  
  &:hover {
    background-color: #E5B913;
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
  
  &:active {
    transform: translateY(-1px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0
