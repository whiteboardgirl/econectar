import Header from './components/Header'

// Honey color palette
const colors = {
  honey: '#FFA000',      // Main honey color
  honeyComb: '#FFB300',  // Lighter honey
  beeYellow: '#FFD54F',  // Light yellow
  darkHoney: '#FF6F00',  // Dark honey
  white: '#FFFFFF'
}

function App() {
  return (
    <>
      <Header colors={colors} />
      <main style={{
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${colors.honey} 0%, ${colors.darkHoney} 100%)`,
        color: colors.white,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        paddingTop: '64px'
      }}>
        <h1 style={{
          fontSize: '3.5rem',
          marginBottom: '1rem',
          textShadow: '2px 2px 4px rgba(0,0,0,0.2)'
        }}>
          Econectar
        </h1>
        <p style={{
          fontSize: '1.5rem',
          marginBottom: '2rem',
          maxWidth: '800px',
          padding: '0 20px',
          textShadow: '1px 1px 2px rgba(0,0,0,0.2)'
        }}>
          Conectando pessoas e abelhas nativas
        </p>
        <a 
          href="#sobre"
          style={{
            backgroundColor: colors.white,
            color: colors.darkHoney,
            padding: '12px 32px',
            borderRadius: '25px',
            textDecoration: 'none',
            fontWeight: 'bold',
            transition: 'all 0.3s ease',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}
          onMouseOver={e => {
            e.target.style.transform = 'translateY(-2px)'
            e.target.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)'
          }}
          onMouseOut={e => {
            e.target.style.transform = 'translateY(0)'
            e.target.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)'
          }}
        >
          Saiba Mais
        </a>
      </main>
    </>
  )
}

export default App
