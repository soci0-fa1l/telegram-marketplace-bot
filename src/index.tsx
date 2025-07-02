import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // 스타일을 원하면 여기에 추가
import App from './App'; // App 컴포넌트를 import

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
