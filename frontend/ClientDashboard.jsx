// src/components/ClientDashboard.jsx
import React, { useState, useEffect } from 'react';
import { api } from '../api';

export default function ClientDashboard() {
  const [profile, setProfile] = useState({ full_name: '', email: '' });
  const [bookings, setBookings] = useState([]);
  const [newBooking, setNewBooking] = useState({ document_name: '', scheduled_time: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Bootstrap CRM profile data and current transactions from your live Cloud Run API
    async function loadClientData() {
      try {
        const profileData = await api.getProfile(); // Points to /api/v1/users/me
        const bookingsData = await api.getBookings(); // Points to /api/v1/notary/sessions
        setProfile(profileData);
        setBookings(bookingsData);
      } catch (err) {
        console.error("Failed to load customer CRM metadata:", err);
      } finally {
        setLoading(false);
      }
    }
    loadClientData();
  }, []);

  const handleBookingSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createNewBooking(newBooking);
      alert("Notary appointment initialized successfully!");
      // Reload bookings list
    } catch (err) {
      alert(`Booking conflict: ${err.message}`);
    }
  };

  if (loading) return <div>Syncing secure client profile container...</div>;

  return (
    <div style={{ padding: '25px', fontFamily: 'sans-serif' }}>
      <h1>👋 Hello, {profile.full_name}</h1>
      
      {/* 1. Profile CRM Card */}
      <section style={{ background: '#f5f5f7', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
        <h3>👤 Your CRM Profile Details</h3>
        <p><strong>Email Access:</strong> {profile.email}</p>
        <button onClick={() => alert("Edit profile endpoint logic connection goes here.")}>Update Profile</button>
      </section>

      {/* 2. Schedule Appointment Form */}
      <section style={{ border: '1px solid #eaeaea', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
        <h3>📅 Request an Online Notarization Session</h3>
        <form onSubmit={handleBookingSubmit}>
          <input 
            type="text" 
            placeholder="Document Name (e.g., Deed of Trust)" 
            value={newBooking.document_name}
            onChange={e => setNewBooking({...newBooking, document_name: e.target.value})}
            required
            style={{ marginRight: '10px', padding: '8px' }}
          />
          <input 
            type="datetime-local" 
            value={newBooking.scheduled_time}
            onChange={e => setNewBooking({...newBooking, scheduled_time: e.target.value})}
            required
            style={{ marginRight: '10px', padding: '8px' }}
          />
          <button type="submit" style={{ background: '#0070f3', color: 'white', border: 'none', padding: '8px 15px', borderRadius: '4px' }}>Book Appointment</button>
        </form>
      </section>

      {/* 3. Real-Time Transaction Ledger */}
      <section>
        <h3>📋 Your Notary Transaction Records</h3>
        <ul>
          {bookings.map(b => (
            <li key={b.id} style={{ padding: '8px 0', borderBottom: '1px solid #eee' }}>
              <strong>{b.document_name}</strong> - Status: <span style={{ color: b.status === 'COMPLETED' ? 'green' : 'orange' }}>{b.status}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
