function Header() {
  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      backgroundColor: 'white',
      padding: '1rem',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      zIndex: 1000
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1 style={{ 
          color: '#2E7D32',
          fontSize: '1.5rem',
          margin: 0
        }}>
          Econectar
        </h1>
        <div style={{ display: 'flex', gap: '2rem' }}>
          <a href="#sobre" style={{ 
            color: '#333', 
            textDecoration: 'none',
            fontWeight: '500'
          }}>Sobre</a>
          <a href="#projetos" style={{ 
            color: '#333', 
            textDecoration: 'none',
            fontWeight: '500'
          }}>Projetos</a>
          <a href="#contato" style={{ 
            color: '#333', 
            textDecoration: 'none',
            fontWeight: '500'
          }}>Contato</a>
        </div>
      </div>
    </nav>
  )
}

export default Header
