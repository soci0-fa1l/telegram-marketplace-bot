// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';  // 이 부분이 제대로 되어 있어야 합니다.
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
