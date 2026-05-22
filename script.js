const { useState, useEffect } = React;

// ===== Navbar =====
function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <nav className={`navbar navbar-expand-lg navbar-dark fixed-top ${scrolled ? 'scrolled' : ''} navbar-custom`}>
      <div className="container">
        <a className="navbar-brand d-flex align-items-center" href="#home">
          <img src="images/sos_large_logo_3.png" alt="Smart Organizational Solutions logo" className="navbar-logo me-2" />
          <span>SOS</span>
        </a>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item"><a className="nav-link" href="#home">Home</a></li>
            <li className="nav-item"><a className="nav-link" href="#features">Services</a></li>
            <li className="nav-item"><a className="nav-link" href="#about">About</a></li>
            <li className="nav-item"><a className="nav-link" href="#contact">Contact</a></li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

// ===== Hero =====
function Hero() {
  return (
    <section className="hero text-white" id="home">
      <div className="container position-relative">
        <div className="row align-items-center">
          <div className="col-lg-7">
            <h1 className="display-4 mb-4">Smart Organizational Solutions</h1>
            <p className="lead mb-4">
              A two-person high-tech consultancy: we combine cutting-edge mobile & AI expertise with organizational effectiveness and change management to help your business perform at its best.
            </p>
            <div className="d-flex flex-wrap gap-3">
              <a href="#contact" className="btn btn-primary">Contact us</a>
              <a href="#about" className="btn btn-outline-light">Meet the team</a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ===== Features (Services) =====
function Features() {
  const items = [
    { icon: 'bi-phone', title: 'Android & mobile', text: 'Expert Android development and applying AI technology to mobile platforms—from strategy to deployment.', color: 'primary' },
    { icon: 'bi-diagram-3', title: 'Organizational effectiveness', text: 'Optimize how your teams and processes work so your organization can deliver results consistently.', color: 'accent' },
    { icon: 'bi-arrow-repeat', title: 'Change management', text: 'Navigate transitions with clarity: we help you plan, communicate, and sustain change that sticks.', color: 'success' },
  ];

  return (
    <section className="features" id="features">
      <div className="container">
        <h2 className="section-title text-center">What we do</h2>
        <p className="section-subtitle text-center">
          Technology and people expertise in one small, focused consultancy.
        </p>
        <div className="row g-4">
          {items.map((item, i) => (
            <div key={i} className="col-md-6 col-lg-4">
              <div className="feature-card card">
                <div className={`feature-icon ${item.color}`}>
                  <i className={`bi ${item.icon}`}></i>
                </div>
                <h5 className="fw-bold">{item.title}</h5>
                <p className="text-secondary mb-0">{item.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ===== About / Team =====
function About() {
  return (
    <section className="about" id="about">
      <div className="container">
        <h2 className="section-title text-center">Our team</h2>
        <p className="section-subtitle text-center">
          A small consultancy with deep expertise in technology and organizations.
        </p>

        <div className="team-vertical">
          <div className="team-section team-section-aprill card border-0 overflow-hidden">
            <div className="team-section-inner">
              <div className="team-photo-wrapper">
                <img src="images/aprill_prof_full.jpg" alt="Aprill Baughns" className="team-photo" />
              </div>
              <div className="team-section-content">
                <p className="team-eyebrow text-primary small fw-semibold mb-2">
                  Transformation &amp; organizational effectiveness
                </p>
                <h3 className="h4 fw-bold mb-1">Aprill Baughns</h3>
                <p className="team-title text-secondary small mb-3">
                  Senior Director Analyst, Gartner · Transformation Architect · Business Behavioral Scientist
                </p>
                <p className="small mb-3">
                  Aprill helps organizations design marketing and communications structures that scale—analyzing
                  how teams develop, transform, and perform so leaders get actionable, evidence-based guidance.
                  She has led complex enterprise change from strategy through delivery, including programs valued
                  in the billions and affecting tens of thousands of employees.
                </p>
                <ul className="team-focus-list small mb-3">
                  <li>Organizational transformation &amp; operational readiness</li>
                  <li>Agile leadership, change management &amp; M&amp;A integration</li>
                  <li>Marketing &amp; communications effectiveness at enterprise scale</li>
                </ul>
                <div className="team-credentials d-flex flex-wrap gap-2 mb-3">
                  <span className="badge rounded-pill text-bg-light border">CCMP™</span>
                  <span className="badge rounded-pill text-bg-light border">CSM®</span>
                  <span className="badge rounded-pill text-bg-light border">CAL</span>
                  <span className="badge rounded-pill text-bg-light border">PMP</span>
                  <span className="badge rounded-pill text-bg-light border">Prosci</span>
                  <span className="badge rounded-pill text-bg-light border">SAFe</span>
                </div>
                <p className="team-quote small fst-italic text-secondary mb-0">
                  &ldquo;While others focus on not breaking the business, my job is to ensure employees aren&rsquo;t broken—while still not breaking the business.&rdquo;
                </p>
              </div>
            </div>
          </div>

          <div className="team-section team-section-andrew card border-0 overflow-hidden">
            <div className="team-section-inner">
              <div className="team-photo-wrapper">
                <img src="images/ugly_andrew.jpg" alt="Andrew Baughns" className="team-photo" />
              </div>
              <div className="team-section-content">
                <p className="team-eyebrow text-primary small fw-semibold mb-2">
                  Mobile development &amp; on-device AI
                </p>
                <h3 className="h4 fw-bold mb-1">Andrew Baughns</h3>
                <p className="team-title text-secondary small mb-3">
                  Mobile Developer · AI Specialist · On-Device AI &amp; Intelligent Applications
                </p>
                <p className="small mb-3">
                  Andrew brings nearly two decades of end-to-end Android experience, from architecture and
                  Play Store delivery to integrating generative AI and large language models on mobile devices.
                  He has led development for telematics platforms, voice assistants, and privacy-focused LLM
                  infrastructure—combining clean architecture, CI/CD, and a top-down, iterative approach to
                  ship intelligently designed apps that are easy to understand and evolve.
                </p>
                <ul className="team-focus-list small mb-3">
                  <li>Android applications, clean architecture &amp; CI/CD at production scale</li>
                  <li>Generative AI, LLMs &amp; intelligent agents on mobile and in the cloud</li>
                  <li>Mobile sensing, geolocation, UX design (Figma) &amp; privacy-conscious platforms</li>
                </ul>
                <div className="team-credentials d-flex flex-wrap gap-2 mb-3">
                  <span className="badge rounded-pill text-bg-light border">Android</span>
                  <span className="badge rounded-pill text-bg-light border">Gen AI</span>
                  <span className="badge rounded-pill text-bg-light border">LLMs</span>
                  <span className="badge rounded-pill text-bg-light border">CI/CD</span>
                  <span className="badge rounded-pill text-bg-light border">MIT</span>
                  <span className="badge rounded-pill text-bg-light border">Georgia Tech MS CS</span>
                </div>
                <p className="team-quote small fst-italic text-secondary mb-0">
                  &ldquo;The goal is not to write perfect code, but code that is easy to understand, change, and aligned with a consistent design approach.&rdquo;
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ===== Contact =====
function Contact() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <section className="contact" id="contact">
      <div className="container">
        <h2 className="section-title text-center">Get in touch</h2>
        <p className="section-subtitle text-center">
          Have a project in mind? Tell us about it and we'll get back to you within 24 hours.
        </p>
        <div className="row justify-content-center">
          <div className="col-lg-8">
            {submitted ? (
              <div className="alert alert-success text-center">
                <i className="bi bi-check-circle-fill me-2"></i>
                Thanks! We've received your message and will be in touch soon.
              </div>
            ) : (
              <form className="contact-form" onSubmit={handleSubmit}>
                <div className="row g-3">
                  <div className="col-md-6">
                    <input type="text" className="form-control" placeholder="Your name" required />
                  </div>
                  <div className="col-md-6">
                    <input type="email" className="form-control" placeholder="Email address" required />
                  </div>
                  <div className="col-12">
                    <select className="form-select">
                      <option value="">What are you interested in?</option>
                      <option value="android-ai">Android & AI on mobile</option>
                      <option value="org-effectiveness">Organizational effectiveness</option>
                      <option value="change-mgmt">Change management</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <div className="col-12">
                    <textarea className="form-control" rows="4" placeholder="Your message" required></textarea>
                  </div>
                  <div className="col-12">
                    <button type="submit" className="btn btn-primary">Send message</button>
                  </div>
                </div>
              </form>
            )}
            <div className="mt-5 pt-4">
              <div className="contact-info-item">
                <i className="bi bi-envelope-fill"></i>
                <div>
                  <strong>Email</strong><br />
                  Use the form above to reach us. We'll respond as soon as we can.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ===== Footer =====
function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="row">
          <div className="col-md-6 mb-4 mb-md-0">
            <span className="navbar-brand text-white">Smart Organizational Solutions, LLC</span>
            <p className="mt-2 mb-3">High-tech consultancy: mobile, AI, and organizational excellence.</p>
            <div className="social-links">
              <a href="#"><i className="bi bi-linkedin"></i></a>
              <a href="#"><i className="bi bi-twitter-x"></i></a>
              <a href="#"><i className="bi bi-github"></i></a>
            </div>
          </div>
          <div className="col-md-3 col-6">
            <h6 className="text-white mb-3">Quick links</h6>
            <ul className="list-unstyled">
              <li><a href="#home">Home</a></li>
              <li><a href="#features">Services</a></li>
              <li><a href="#about">About</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>
          <div className="col-md-3 col-6">
            <h6 className="text-white mb-3">Legal</h6>
            <ul className="list-unstyled">
              <li><a href="#">Privacy</a></li>
              <li><a href="#">Terms</a></li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom text-center text-md-start">
          &copy; {new Date().getFullYear()} Smart Organizational Solutions, LLC. All rights reserved.
        </div>
      </div>
    </footer>
  );
}

// ===== App =====
function App() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <Features />
        <About />
        <Contact />
        <Footer />
      </main>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
