import { useState } from 'react';
import { ArrowLeft, X } from 'lucide-react';
import projectsData from './projects.json';

type ProjectFile = {
  id: string;
  title: string;
  full: string;
  thumb: string;
  type: string;
};

type ProjectData = {
  id: string;
  name: string;
  profession?: string;
  stage?: string;
  description?: string;
  cover: string | null;
  files: ProjectFile[];
};

const projects: ProjectData[] = projectsData;

function App() {
  const [selectedProject, setSelectedProject] = useState<ProjectData | null>(null);
  const [selectedImage, setSelectedImage] = useState<ProjectFile | null>(null);

  const currentIndex = selectedProject && selectedImage 
    ? selectedProject.files.findIndex(f => f.id === selectedImage.id)
    : -1;

  if (selectedImage && selectedProject) {
    window.onkeydown = (e) => {
      if (e.key === 'Escape') setSelectedImage(null);
      if (e.key === 'ArrowRight' && currentIndex < selectedProject.files.length - 1) {
        setSelectedImage(selectedProject.files[currentIndex + 1]);
      }
      if (e.key === 'ArrowLeft' && currentIndex > 0) {
        setSelectedImage(selectedProject.files[currentIndex - 1]);
      }
    };
  } else {
    window.onkeydown = null;
  }

  // Prevent crash if projects.json is still in the old format (script is still running)
  if (!Array.isArray(projects)) {
    return (
      <div className="app-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <h1 className="hero-title" style={{ fontSize: '3rem', marginBottom: '1rem' }}>Generuje sa portfólio...</h1>
        <p className="hero-subtitle">Skript práve spracováva výkresy do vysokej kvality. O chvíľu to bude hotové.</p>
        <p style={{ marginTop: '2rem', color: '#6b7280' }}>(Stránku si môžete za pár minút obnoviť)</p>
      </div>
    );
  }

  const topProjects = [
    "RD Imričko", // Replaces RD VALUL
    "EDU-TECH KAMPUS", // Matches EDU-TECH KAMPUS PÚCHOV
    "ASOC", // Replaces ADM Komarnianska
    "Chata na Jankovej Lúke",
    "Obecny dom Limbach",
    "TTP - FaxCopy"
  ];
  
  const demotedProjects = [
    "RD Veľká Paka",
    "RD POD PRIEHRADOU"
  ];
  
  const sortedProjects = [...projects].sort((a, b) => {
    // 1. Skontrolujeme či sú v top zozname
    const topA = topProjects.findIndex(p => a.name.includes(p) || p.includes(a.name));
    const topB = topProjects.findIndex(p => b.name.includes(p) || p.includes(b.name));
    
    if (topA !== -1 && topB !== -1) return topA - topB; // obidva sú v top, zoradíme podľa top indexu
    if (topA !== -1) return -1; // iba A je v top
    if (topB !== -1) return 1;  // iba B je v top
    
    // 2. Skontrolujeme či sú v demoted zozname (na koniec)
    const demoteA = demotedProjects.findIndex(p => a.name.includes(p) || p.includes(a.name));
    const demoteB = demotedProjects.findIndex(p => b.name.includes(p) || p.includes(b.name));
    
    if (demoteA !== -1 && demoteB !== -1) return demoteA - demoteB;
    if (demoteA !== -1) return 1;
    if (demoteB !== -1) return -1;
    
    // 3. Ak nie sú ani v jednom, zoradíme abecedne
    return a.name.localeCompare(b.name);
  });

  return (
    <div className="app-container" onContextMenu={(e) => e.preventDefault()}>
      {!selectedProject ? (
        <>
          <div className="hero">
            <div className="hero-text">
              <h1 className="hero-title">Portfólio Projektov</h1>
              <p className="hero-subtitle">ING. Viktor Labovský</p>
              <div className="hero-contact">
                <a href="mailto:labovskyviktor@gmail.com">labovskyviktor@gmail.com</a>
                <a href="tel:+421915341479">+421 915 341 479</a>
              </div>
            </div>
            <img src="/profile-photo.png" alt="Ing. Viktor Labovský" className="profile-photo" />
          </div>
          
          <main className="main-content">
            <h2 className="section-title">Vybrané Práce</h2>
            <div className="project-grid">
              {sortedProjects.map((project) => (
                <div 
                  key={project.id} 
                  className="project-card"
                  onClick={() => setSelectedProject(project)}
                >
                  {project.cover ? (
                    <img src={project.cover} alt={project.name} className="project-cover" loading="lazy" />
                  ) : (
                    <div className="project-cover" style={{ background: '#e5e7eb' }}></div>
                  )}
                  <div className="project-overlay">
                    <h3 className="project-title">{project.name}</h3>
                    {project.profession && (
                      <p className="project-meta">
                        {project.profession}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </main>
        </>
      ) : (
        <main className="main-content">
          <button className="back-button" onClick={() => setSelectedProject(null)}>
            <ArrowLeft size={20} /> Zoznam projektov
          </button>
          
          <div className="detail-header">
            <h2 className="project-detail-title">{selectedProject.name}</h2>
            {(selectedProject.profession || selectedProject.stage) ? (
              <p className="hero-subtitle">
                {selectedProject.profession} {selectedProject.stage && `• ${selectedProject.stage}`}
              </p>
            ) : (
              <p className="hero-subtitle">Detail Projektu</p>
            )}
            {selectedProject.description && (
              <p className="project-description">
                {selectedProject.description}
              </p>
            )}
          </div>
          
          <div className="image-grid">
            {selectedProject.files.map((file) => (
              <div 
                key={file.id} 
                className="image-card"
                onClick={() => setSelectedImage(file)}
              >
                <div className="img-wrapper">
                  {/* Notice we use the 'thumb' for grid loading to be super fast */}
                  <img src={file.thumb} alt={file.title} loading="lazy" />
                </div>
                <div className="image-info">
                  <h3 className="image-title">{file.title}</h3>
                  <p className="image-type">{file.type === 'drawing' ? 'Výkres' : 'Dokument'}</p>
                </div>
              </div>
            ))}
          </div>
        </main>
      )}

      {/* Lightbox Modal */}
      {selectedImage && selectedProject && (
        <div 
          className="lightbox-overlay"
          onClick={() => setSelectedImage(null)}
        >
          <div className="lightbox-toolbar" onClick={(e) => e.stopPropagation()}>
            <h3 className="lightbox-title">{selectedImage.title} ({currentIndex + 1} / {selectedProject.files.length})</h3>
            <div className="lightbox-actions">

              <button 
                className="lightbox-btn" 
                onClick={() => setSelectedImage(null)} 
                title="Zavrieť"
              >
                <X size={24} />
              </button>
            </div>
          </div>
          
          <div className="lightbox-content-wrapper" onClick={(e) => e.stopPropagation()}>
            <button 
              className="lightbox-nav-btn left" 
              onClick={() => currentIndex > 0 && setSelectedImage(selectedProject.files[currentIndex - 1])}
              style={{ visibility: currentIndex > 0 ? 'visible' : 'hidden' }}
            >
              &larr;
            </button>

            <div className="scrollable-image-container" style={{ position: 'relative', width: '90vw', height: '90vh', padding: 0 }}>
              {/* Ochranná vrstva hore (blokuje horné skryté lišty) */}
              <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '60px', zIndex: 10, cursor: 'default' }} />
              
              <iframe 
                src={`${selectedImage.full}#toolbar=0&navpanes=0&scrollbar=0&view=FitH`} 
                width="100%" 
                height="100%" 
                style={{ border: 'none' }} 
              />
              
              {/* Ochranná vrstva vpravo (blokuje niektoré bočné tlačidlá) */}
              <div style={{ position: 'absolute', top: 0, right: 0, bottom: 0, width: '60px', zIndex: 10, cursor: 'default' }} />
              
              {/* Ochranná vrstva dole (blokuje plávajúce tlačidlá na stiahnutie) */}
              <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: '80px', zIndex: 10, cursor: 'default' }} />
            </div>

            <button 
              className="lightbox-nav-btn right" 
              onClick={() => currentIndex < selectedProject.files.length - 1 && setSelectedImage(selectedProject.files[currentIndex + 1])}
              style={{ visibility: currentIndex < selectedProject.files.length - 1 ? 'visible' : 'hidden' }}
            >
              &rarr;
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
