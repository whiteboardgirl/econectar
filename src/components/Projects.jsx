import { useState } from 'react'
import styled from 'styled-components'

const ProjectsSection = styled.section`
  padding: 6rem 2rem;
  background-color: white;
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

const ProjectsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  
  @media (max-width: 400px) {
    grid-template-columns: 1fr;
  }
`

const ProjectCard = styled.div`
  background-color: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
  }
`

const ProjectImage = styled.div`
  height: 200px;
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
  
  ${ProjectCard}:hover & img {
    transform: scale(1.1);
  }
`

const ProjectContent = styled.div`
  padding: 1.5rem;
`

const ProjectTitle = styled.h3`
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
  color: #333;
`

const ProjectDescription = styled.p`
  font-size: 1rem;
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.6;
`

const ProjectLink = styled.a`
  display: inline-block;
  color: #F1C40F;
  font-weight: 600;
  text-decoration: none;
  
  &:hover {
    text-decoration: underline;
  }
`

const Projects = () => {
  const projectsData = [
    {
      id: 1,
      title: "Conservation Initiatives",
      description: "Our efforts to protect natural habitats and create safe environments for stingless bee populations to thrive.",
      image: "/assets/images/projects/project1.jpg",
      link: "#"
    },
    {
      id: 2,
      title: "Sustainable Meliponiculture",
      description: "Teaching communities sustainable practices for keeping stingless bees and harvesting their honey and propolis.",
      image: "/assets/images/projects/project2.jpg",
      link: "#"
    },
    {
      id: 3,
      title: "Research & Education",
      description: "Ongoing scientific studies on stingless bee behavior, ecology, and their role in maintaining biodiversity.",
      image: "/assets/images/projects/project3.jpg",
      link: "#"
    }
  ]
  
  return (
    <ProjectsSection id="projects">
      <Container>
        <SectionTitle>Our Projects</SectionTitle>
        
        <ProjectsGrid>
          {projectsData.map(project => (
            <ProjectCard key={project.id}>
              <ProjectImage>
                <img src={project.image} alt={project.title} />
              </ProjectImage>
              <ProjectContent>
                <ProjectTitle>{project.title}</ProjectTitle>
                <ProjectDescription>{project.description}</ProjectDescription>
                <ProjectLink href={project.link}>Learn more →</ProjectLink>
              </ProjectContent>
            </ProjectCard>
          ))}
        </ProjectsGrid>
      </Container>
    </ProjectsSection>
  )
}

export default Projects
