function About({ colors }) {
  return (
    <section id="sobre" style={{
      padding: '80px 20px',
      backgroundColor: colors.white,
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Honeycomb Pattern Background */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        opacity: 0.05,
        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0l30 15v30L0 60z' fill='%23${colors.honey.slice(1)}' fill-opacity='0.5'/%3E%3Cpath d='M30 15l30-15v60L30 45z' fill='%23${colors.honey.slice(1)}' fill-opacity='0.5'/%3E%3C/svg%3E")`,
        backgroundSize: '60px 60px'
      }} />

      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        position: 'relative',
        zIndex: 1
      }}>
        <h2 style={{
          color: colors.darkHoney,
          fontSize: '2.5rem',
          marginBottom: '2rem',
          textAlign: 'center'
        }}>
          Sobre Nós
        </h2>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '2rem',
          alignItems: 'center'
        }}>
          {/* Text Content */}
          <div>
            <h3 style={{
              color: colors.honey,
              fontSize: '1.8rem',
              marginBottom: '1rem'
            }}>
              Nossa Missão
            </h3>
            <p style={{
              color: '#666',
              lineHeight: 1.6,
              marginBottom: '1.5rem'
            }}>
              Promovemos a preservação das abelhas nativas através da meliponicultura sustentável, 
              conectando comunidades tradicionais, agricultores e amantes da natureza.
            </p>

            <h3 style={{
              color: colors.honey,
              fontSize: '1.8rem',
              marginBottom: '1rem'
            }}>
              Nossa Visão
            </h3>
            <p style={{
              color: '#666',
              lineHeight: 1.6
            }}>
              Buscamos um mundo onde a harmonia entre seres humanos e abelhas nativas 
              fortaleça a biodiversidade e promova o desenvolvimento sustentável local.
            </p>
          </div>

          {/* Stats/Features */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: '1.5rem'
          }}>
            {[
              { number: '100+', text: 'Meliponicultores' },
              { number: '20+', text: 'Espécies Nativas' },
              { number: '500+', text: 'Colmeias' },
              { number: '10+', text: 'Comunidades' }
            ].map((stat, index) => (
              <div key={index} style={{
                backgroundColor: colors.white,
                padding: '1.5rem',
                borderRadius: '8px',
                textAlign: 'center',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                border: `2px solid ${colors.beeYellow}`,
                transition: 'transform 0.3s ease'
              }}>
                <h4 style={{
                  color: colors.darkHoney,
                  fontSize: '2rem',
                  marginBottom: '0.5rem'
                }}>
                  {stat.number}
                </h4>
                <p style={{
                  color: '#666',
                  fontSize: '1rem'
                }}>
                  {stat.text}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default About
