function Hero() {
  return (
    <div style={{
      minHeight: '90vh',
      backgroundColor: '#2E7D32',
      color: 'white',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
      padding: '0 20px'
    }}>
      <div style={{ maxWidth: '800px' }}>
        <h1 style={{ 
          fontSize: '3.5rem', 
          marginBottom: '1rem' 
        }}>
          Conectando Pessoas e Abelhas Nativas
        </h1>
        <p style={{ 
          fontSize: '1.5rem', 
          marginBottom: '2rem' 
        }}>
          Através da meliponicultura sustentável, preservamos a biodiversidade
          e promovemos o desenvolvimento local
        </p>
        <a 
          href="#sobre" 
          style={{
            display: 'inline-block',
            padding: '1rem 2rem',
            backgroundColor: 'white',
            color: '#2E7D32',
            textDecoration: 'none',
            borderRadius: '5px',
            fontWeight: 'bold'
          }}
        >
          Saiba Mais
        </a>
      </div>
    </div>
  )
}

export default Hero
