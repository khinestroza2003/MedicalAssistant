#!/usr/bin/env python3
import os
import json

base_path = '/Users/kevinhinestroza/Documents/Redes y Telematicas/AsistenteMedico/asistente_medico'

files = {
    'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Asistente Médico</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
''',
    
    'package.json': '''{
  "name": "asistente_medico",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.8"
  }
}
''',

    'vite.config.js': '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
  },
})
''',

    '.gitignore': '''node_modules/
dist/
.DS_Store
.env.local
.env.*.local
*.log
.vite/
''',

    'README.md': '''# Asistente Médico - Frontend

React + Vite medical assistant frontend.

## Setup
npm install && npm run dev
''',

    'src/main.jsx': '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
''',

    'src/App.jsx': '''import Login from './components/Login';
import './App.css';

function App() {
  return (
    <div className="app">
      <Login />
    </div>
  );
}

export default App;
''',

    'src/App.css': '''#root {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
}

.app {
  flex: 1;
}
''',

    'src/index.css': ''':root {
  --primary: #667eea;
  --primary-dark: #764ba2;
  --primary-light: #f093fb;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
  --bg-white: #ffffff;
  --border-color: #e5e7eb;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--bg-light);
  color: var(--text-dark);
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: var(--spacing-md);
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }

p {
  color: var(--text-light);
  margin-bottom: var(--spacing-md);
}

input, textarea, select {
  font-family: inherit;
  font-size: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: var(--spacing-sm) var(--spacing-md);
  transition: all 0.3s ease;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

button {
  cursor: pointer;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

a {
  color: var(--primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: var(--primary-dark);
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-light);
}

::-webkit-scrollbar-thumb {
  background: var(--primary);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--primary-dark);
}
''',

    'src/components/Login.jsx': '''import SymptomsSelector from './SymptomsSelector';
import './Login.css';

export default function Login() {
  return (
    <div className="login-container">
      <div className="blob blob-1"></div>
      <div className="blob blob-2"></div>
      <div className="blob blob-3"></div>

      <div className="login-content">
        <div className="logo-circle">
          <span className="logo-text">⚕️</span>
        </div>
        
        <h1>Asistente Médico</h1>
        <p className="subtitle">Describe tus síntomas para recibir diagnósticos personalizados</p>
        
        <SymptomsSelector />
        
        <p className="disclaimer">
          Nota: Este sistema es informativo. Consulta a un médico profesional para diagnósticos precisos.
        </p>
      </div>
    </div>
  );
}
''',

    'src/components/Login.css': '''.login-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  padding: var(--spacing-lg);
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  opacity: 0.2;
  filter: blur(40px);
}

.blob-1 {
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.5);
  top: -100px;
  left: -100px;
  animation: float 20s infinite ease-in-out;
}

.blob-2 {
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.3);
  bottom: -50px;
  right: -50px;
  animation: float 25s infinite ease-in-out;
}

.blob-3 {
  width: 350px;
  height: 350px;
  background: rgba(255, 255, 255, 0.4);
  top: 50%;
  right: 10%;
  animation: float 22s infinite ease-in-out;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, 30px); }
}

.login-content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: var(--spacing-2xl);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.logo-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--spacing-xl);
  animation: bounce 2s ease-in-out infinite;
}

.logo-text {
  font-size: 50px;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.login-content h1 {
  color: var(--text-dark);
  margin-bottom: var(--spacing-sm);
}

.subtitle {
  color: var(--text-light);
  font-size: 1.1rem;
  margin-bottom: var(--spacing-xl);
}

.disclaimer {
  font-size: 0.9rem;
  color: var(--text-light);
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

@media (max-width: 768px) {
  .login-container {
    padding: var(--spacing-md);
  }

  .login-content {
    padding: var(--spacing-lg);
    border-radius: 16px;
  }

  .login-content h1 {
    font-size: 1.8rem;
  }

  .blob-1, .blob-2, .blob-3 {
    display: none;
  }
}
''',

    'src/components/SymptomsSelector.jsx': '''import { useState, useEffect, useMemo } from 'react';
import './SymptomsSelector.css';

export default function SymptomsSelector() {
  const [symptoms, setSymptoms] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8080/api/diagnostico/sintomas')
      .then(res => res.json())
      .then(data => {
        setSymptoms(data);
        setLoading(false);
      })
      .catch(() => {
        console.error('Error fetching symptoms');
        setLoading(false);
      });
  }, []);

  const filteredSuggestions = useMemo(() => {
    if (!searchTerm.trim()) return [];
    const selected = selectedSymptoms.map(s => s.toLowerCase());
    return symptoms
      .filter(sym => 
        sym.nombre.toLowerCase().includes(searchTerm.toLowerCase()) &&
        !selected.includes(sym.nombre.toLowerCase())
      )
      .slice(0, 8);
  }, [searchTerm, symptoms, selectedSymptoms]);

  const handleAddSymptom = (symptom) => {
    if (!selectedSymptoms.find(s => s === symptom.nombre)) {
      setSelectedSymptoms([...selectedSymptoms, symptom.nombre]);
    }
    setSearchTerm('');
    setShowSuggestions(false);
  };

  const handleRemoveSymptom = (symptom) => {
    setSelectedSymptoms(selectedSymptoms.filter(s => s !== symptom));
  };

  const handleSubmit = () => {
    if (selectedSymptoms.length > 0) {
      console.log('Síntomas seleccionados:', selectedSymptoms);
    }
  };

  return (
    <div className="symptoms-selector">
      <div className="search-wrapper">
        <input
          type="text"
          placeholder="Busca tus síntomas..."
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setShowSuggestions(true);
          }}
          onFocus={() => setShowSuggestions(true)}
          className="search-input"
        />

        {showSuggestions && filteredSuggestions.length > 0 && (
          <div className="suggestions-dropdown">
            {filteredSuggestions.map((symptom) => (
              <div
                key={symptom.id}
                className="suggestion-item"
                onClick={() => handleAddSymptom(symptom)}
              >
                {symptom.nombre}
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedSymptoms.length > 0 && (
        <div className="selected-symptoms">
          {selectedSymptoms.map((symptom) => (
            <div key={symptom} className="symptom-chip">
              {symptom}
              <button
                className="remove-btn"
                onClick={() => handleRemoveSymptom(symptom)}
                aria-label="Remove symptom"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      )}

      <button
        className="next-button"
        onClick={handleSubmit}
        disabled={selectedSymptoms.length === 0 || loading}
      >
        {loading ? 'Cargando...' : 'Continuar'}
      </button>
    </div>
  );
}
''',

    'src/components/SymptomsSelector.css': '''.symptoms-selector {
  width: 100%;
  margin-top: var(--spacing-xl);
}

.search-wrapper {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 14px 18px;
  font-size: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 50px;
  background: var(--bg-white);
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-white);
  border: 1px solid var(--border-color);
  border-top: none;
  border-radius: 0 0 12px 12px;
  max-height: 360px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: var(--shadow-lg);
}

.suggestion-item {
  padding: 12px 18px;
  cursor: pointer;
  transition: background 0.2s ease;
  color: var(--text-dark);
}

.suggestion-item:hover {
  background: var(--bg-light);
  color: var(--primary);
}

.selected-symptoms {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: var(--spacing-md);
  padding: var(--spacing-md);
  background: rgba(102, 126, 234, 0.05);
  border-radius: 12px;
}

.symptom-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(102, 126, 234, 0.15);
  color: var(--primary-dark);
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 500;
}

.remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  padding: 0;
  margin: 0;
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1.2rem;
  transition: opacity 0.2s ease;
}

.remove-btn:hover {
  opacity: 0.7;
}

.next-button {
  width: 100%;
  padding: 14px 24px;
  margin-top: var(--spacing-lg);
  font-size: 1rem;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.next-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.next-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .search-input {
    padding: 12px 16px;
    font-size: 0.95rem;
  }

  .selected-symptoms {
    gap: 8px;
    padding: var(--spacing-sm);
  }

  .symptom-chip {
    padding: 6px 12px;
    font-size: 0.9rem;
  }
}
''',

    'src/components/common.css': '''.card {
  background: var(--bg-white);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.alert {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: 8px;
  margin-bottom: var(--spacing-md);
}

.alert-info {
  background: rgba(59, 130, 246, 0.1);
  color: #1e40af;
  border-left: 4px solid #3b82f6;
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  color: #065f46;
  border-left: 4px solid #10b981;
}

.alert-warning {
  background: rgba(245, 158, 11, 0.1);
  color: #78350f;
  border-left: 4px solid #f59e0b;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  color: #7f1d1d;
  border-left: 4px solid #ef4444;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-primary {
  background: rgba(102, 126, 234, 0.2);
  color: var(--primary-dark);
}

.badge-success {
  background: rgba(16, 185, 129, 0.2);
  color: #065f46;
}

.badge-warning {
  background: rgba(245, 158, 11, 0.2);
  color: #78350f;
}

.badge-error {
  background: rgba(239, 68, 68, 0.2);
  color: #7f1d1d;
}
'''
}

for file_path, content in files.items():
    full_path = os.path.join(base_path, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content)
    print(f'Created: {file_path}')

print('All files created successfully!')
