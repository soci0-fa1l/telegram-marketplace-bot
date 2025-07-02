// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';  // 이 부분이 제대로 되어 있어야 합니다.
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
