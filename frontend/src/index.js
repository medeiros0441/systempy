import React from 'react';
import { createRoot } from 'react-dom/client'; // Importa createRoot
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css'; // Importa o CSS do Bootstrap
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'src/assets/css/Global.css'
import 'bootstrap-icons/font/bootstrap-icons.css';

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
    <App />
);
