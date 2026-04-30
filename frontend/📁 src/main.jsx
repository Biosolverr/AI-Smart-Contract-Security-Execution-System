import React from 'react'
import ReactDOM from 'react-dom/client'
import GenRouteUI from './GenRouteUI'
import './index.css' // Предполагается наличие базовых стилей

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <GenRouteUI />
  </React.StrictMode>,
)
