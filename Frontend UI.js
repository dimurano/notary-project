import React, { useState, useEffect } from 'react';

export default function NotarySigningView({ agreementId }) {
  const [signingUrl, setSigningUrl] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch the embeddable URL from your FastAPI backend
    fetch(`/api/v1/notary/signing-url/${agreementId}`)
      .then((res) => res.json())
      .then((data) => {
        setSigningUrl(data.signing_url);
        setLoading(false);
      })
      .catch((err) => console.error("Error loading signing session:", err));
  }, [agreementId]);

  if (loading) return <div>Setting up your secure signing room...</div>;

  return (
    <div style={{ width: '100%', height: '90vh', padding: '10px' }}>
      <div style={{ marginBottom: '10px', display: 'flex', justifyContent: 'space-between' }}>
        <h3>🔒 Secure Notary Signing Portal</h3>
        <p>Please review and sign the document below.</p>
      </div>

      {/* Embedded Adobe Acrobat Sign Frame */}
      
    </div>
  );
}
