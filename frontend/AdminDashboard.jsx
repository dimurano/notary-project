// src/components/AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState({ total_users: 0, pending_signatures: 0 });
  const [allSessions, setAllSessions] = useState([]);
  const [homepageNotice, setHomepageNotice] = useState('');

  useEffect(() => {
    async function loadAdminMetrics() {
      try {
        // Restricted endpoints requiring admin flagged JWT tokens
        const stats = await api.getSystemMetrics(); 
        const logs = await api.getAllGlobalSessions();
        setMetrics(stats);
        setAllSessions(logs);
      } catch (err) {
        console.error("Access Denied: Non-administrative personnel credentials.", err);
      }
    }
    loadAdminMetrics();
  }, []);

  const handleUpdateNotice = async () => {
    try {
      await api.updateFrontendConfig({ alert_notice: homepageNotice });
      alert("Frontend broadcast notice successfully applied to the client view!");
    } catch (err) {
      alert("Configuration write failure.");
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      {/* Sidebar Navigation */}
      <div style={{ width: '250px', background: '#111', color: 'white', padding: '20px' }}>
        <h2>🛡️ Notary Admin</h2>
        <p style={{ color: '#888' }}>System Overviews</p>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ padding: '10px 0', cursor: 'pointer' }}>📈 Live Infrastructure Logs</li>
          <li style={{ padding: '10px 0', cursor: 'pointer' }}>⚙️ Frontend Page Content CMS</li>
          <li style={{ padding: '10px 0', cursor: 'pointer' }}>👥 Identity Verification Review</li>
        </ul>
      </div>

      {/* Main Administrative Action Desk */}
      <div style={{ flexGrow: 1, padding: '30px', background: '#fafafa' }}>
        <h2>System Monitoring Center</h2>
        
        {/* Metric Counter Banner */}
        <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', flex: 1 }}>
            <h4>Total Active CRM Profiles</h4>
            <h2 style={{ color: '#0070f3' }}>{metrics.total_users}</h2>
          </div>
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', flex: 1 }}>
            <h4>Adobe Agreements Pending Signature</h4>
            <h2 style={{ color: '#ff0000' }}>{metrics.pending_signatures}</h2>
          </div>
        </div>

        {/* Global Content Manager System Control (CMS Widget) */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', marginBottom: '30px' }}>
          <h3>✏️ Edit Frontend Home Announcement Bar</h3>
          <textarea 
            rows="3" 
            value={homepageNotice} 
            onChange={e => setHomepageNotice(e.target.value)}
            placeholder="Type temporary system alerts or holiday closures here..." 
            style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
          />
          <button onClick={handleUpdateNotice} style={{ background: '#111', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Publish Live Configuration Changes
          </button>
        </div>
      </div>
    </div>
  );
}
