import Header from './components/Header'

function App() {
  return (
    <>
      <Header />
      <main style={{
        minHeight: '100vh',
        backgroundColor: '#2E7D32',
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        paddingTop: '64px' // Add space for fixed header
      }}>
        <h1 style={{
          fontSize: '3.5rem',
          marginBottom: '1rem'
        }}>
          Econectar
        </h1>
        <p style={{
          fontSize: '1.5rem',
          marginBottom: '2rem',
          maxWidth: '800px',
          padding: '0 20px'
        }}>
          Conectando pessoas e abelhas nativas
        </p>
        <a 
          href="#sobre"
          style={{
            backgroundColor: 'white',
            color: '#2E7D32',
            padding: '12px 24px',
            borderRadius: '4px',
            textDecoration: 'none',
            fontWeight: 'bold',
            transition: 'transform 0.2s ease'
          }}
          onMouseOver={e => e.target.style.transform = 'translateY(-2px)'}
          onMouseOut={e => e.target.style.transform = 'translateY(0)'}
        >
          Saiba Mais
        </a>
      </main>
    </>
  )
}

export default App
