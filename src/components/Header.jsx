function Header({ colors }) {
  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      backgroundColor: colors.white,
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
          color: colors.honey,
          fontSize: '1.5rem',
          margin: 0,
          fontWeight: 'bold'
        }}>
          Econectar
        </h1>
        <div style={{ display: 'flex', gap: '2rem' }}>
          {['Sobre', 'Projetos', 'Contato'].map((item) => (
            <a 
              key={item}
              href={`#${item.toLowerCase()}`} 
              style={{ 
                color: colors.darkHoney,
                textDecoration: 'none',
                fontWeight: '500',
                transition: 'color 0.3s ease'
              }}
              onMouseOver={e => e.target.style.color = colors.honey}
              onMouseOut={e => e.target.style.color = colors.darkHoney}
            >
              {item}
            </a>
          ))}
        </div>
      </div>
    </nav>
  )
}

export default Header
