import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';
import '../../design-system/tokens.css';
import '../../design-system/components/bundle.css';
import './styles.css';

// The design-system bundle is a classic script that reads window.React and
// assigns window.Cashout. Load it once, then render the site.
window.React = React;
window.ReactDOM = ReactDOM;

async function start() {
  await import('../../design-system/components/bundle.js');
  const { default: App } = await import('./App.jsx');
  createRoot(document.getElementById('root')).render(<App />);
}
start();
