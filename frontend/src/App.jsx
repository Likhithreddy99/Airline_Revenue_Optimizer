import { useState, useEffect } from 'react'
import axios from 'axios'
import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis,
  BarChart, Bar, Legend, Cell
} from 'recharts'
import { LineChart, LayoutDashboard, Plane, Map } from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

export default function App() {
  const [activeTab, setActiveTab] = useState('prediction')

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo-container">
          <img src="/logo.png" alt="ARO Logo" className="logo" />
          <div className="logo-text">Airline Revenue<br/>Optimizer</div>
        </div>
        <nav className="nav-links">
          <div 
            className={`nav-item ${activeTab === 'prediction' ? 'active' : ''}`}
            onClick={() => setActiveTab('prediction')}
          >
            <LineChart size={20} /> Optimization Tool
          </div>
          <div 
            className={`nav-item ${activeTab === 'urgency' ? 'active' : ''}`}
            onClick={() => setActiveTab('urgency')}
          >
            <LayoutDashboard size={20} /> Urgency Matrix
          </div>
          <div 
            className={`nav-item ${activeTab === 'route' ? 'active' : ''}`}
            onClick={() => setActiveTab('route')}
          >
            <Map size={20} /> Route Profitability
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'prediction' && <PredictionTool />}
        {activeTab === 'urgency' && <UrgencyMatrix />}
        {activeTab === 'route' && <RouteProfitability />}
      </main>
    </div>
  )
}

function PredictionTool() {
  const [formData, setFormData] = useState({
    days_left: 15,
    seats_remaining: 50,
    is_holiday: false,
    is_weekend: false,
    season: 'Peak',
    flight_type: 'Short Haul',
    class_type: 'Economy',
    operating_cost: 5000.0
  })
  
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handlePredict = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await axios.post(`${API_BASE}/predict_optimal_price`, formData)
      setResult(res.data)
    } catch (err) {
      console.error(err)
      alert("Error calculating optimal price. Make sure backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <header className="header">
        <h1 className="header-title">Dynamic Price Optimization</h1>
        <p className="header-subtitle">Input flight details to calculate the mathematically optimal ticket price that maximizes revenue.</p>
      </header>

      <div className="grid-2">
        <div className="card">
          <form onSubmit={handlePredict}>
            <div className="grid-2">
              <div className="input-group">
                <label>Days Left to Departure</label>
                <input type="number" className="input-control" value={formData.days_left} onChange={(e)=>setFormData({...formData, days_left: parseInt(e.target.value)})} min="1" max="60"/>
              </div>
              <div className="input-group">
                <label>Seats Remaining</label>
                <input type="number" className="input-control" value={formData.seats_remaining} onChange={(e)=>setFormData({...formData, seats_remaining: parseInt(e.target.value)})} min="1"/>
              </div>
              <div className="input-group">
                <label>Season</label>
                <select className="input-control" value={formData.season} onChange={(e)=>setFormData({...formData, season: e.target.value})}>
                  <option>Peak</option>
                  <option>Off-Peak</option>
                  <option>Shoulder</option>
                </select>
              </div>
              <div className="input-group">
                <label>Flight Type</label>
                <select className="input-control" value={formData.flight_type} onChange={(e)=>setFormData({...formData, flight_type: e.target.value})}>
                  <option>Short Haul</option>
                  <option>Medium Haul</option>
                  <option>Long Haul</option>
                </select>
              </div>
              <div className="input-group">
                <label>Class</label>
                <select className="input-control" value={formData.class_type} onChange={(e)=>setFormData({...formData, class_type: e.target.value})}>
                  <option>Economy</option>
                  <option>Business</option>
                </select>
              </div>
              <div className="input-group" style={{ display: 'none' }}>
                {/* Dummy column spacer */}
              </div>
              <div className="input-group" style={{ flexDirection: 'row', alignItems: 'center', gap: '1rem' }}>
                <input type="checkbox" checked={formData.is_holiday} onChange={(e)=>setFormData({...formData, is_holiday: e.target.checked})} />
                <label style={{margin:0}}>Is Holiday?</label>
              </div>
              <div className="input-group" style={{ flexDirection: 'row', alignItems: 'center', gap: '1rem' }}>
                <input type="checkbox" checked={formData.is_weekend} onChange={(e)=>setFormData({...formData, is_weekend: e.target.checked})} />
                <label style={{margin:0}}>Is Weekend?</label>
              </div>
            </div>
            
            <div className="input-group" style={{ marginTop: '1rem' }}>
              <label>Operating Cost (₹)</label>
              <input type="number" className="input-control" value={formData.operating_cost} onChange={(e)=>setFormData({...formData, operating_cost: parseFloat(e.target.value)})} />
            </div>

            <button type="submit" className="btn" disabled={loading} style={{marginTop: '1.5rem'}}>
              {loading ? "Calculating..." : "Find Optimal Price"}
            </button>
          </form>
        </div>

        {result && (
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <h3 style={{marginTop:0, color: 'var(--text-primary)'}}>Optimization Results</h3>
            
            <div className="metric-card" style={{ backgroundColor: 'var(--accent-color)', color: 'white' }}>
              <span style={{ fontSize: '0.875rem', opacity: 0.9 }}>AI Optimal Ticket Price</span>
              <span style={{ fontSize: '3rem', fontWeight: 800 }}>₹{result.optimal_price.toFixed(2)}</span>
            </div>

            <div className="grid-2">
              <div className="metric-card">
                <span className="metric-title">Predicted Demand</span>
                <span className="metric-value">{result.predicted_demand} pax</span>
              </div>
              <div className="metric-card">
                <span className="metric-title">Estimated Revenue</span>
                <span className="metric-value success">₹{result.estimated_revenue.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}</span>
              </div>
            </div>
            
            <div className="metric-card">
                <span className="metric-title">Estimated Profit (Revenue - Cost)</span>
                <span className="metric-value accent">₹{result.estimated_profit.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function UrgencyMatrix() {
  const [data, setData] = useState([])

  useEffect(() => {
    axios.get(`${API_BASE}/urgency_data`).then(res => setData(res.data.data)).catch(console.error)
  }, [])

  return (
    <div>
      <header className="header">
        <h1 className="header-title">Urgency Matrix</h1>
        <p className="header-subtitle">Identify distressed inventory across the flight network.</p>
      </header>

      <div className="card" style={{ height: '600px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis type="number" dataKey="days_left" name="Days to Departure" tickCount={10} />
            <YAxis type="number" dataKey="seats_remaining" name="Seats Remaining" />
            <ZAxis type="number" dataKey="load_factor" range={[50, 400]} name="Load Factor" />
            <Tooltip 
              cursor={{ strokeDasharray: '3 3' }} 
              content={({ payload }) => {
                if (!payload || !payload.length) return null;
                const d = payload[0].payload;
                return (
                  <div style={{ background: '#fff', padding: '1rem', border: '1px solid #ccc', borderRadius: '0.5rem', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}>
                    <strong>Flight {d.flight}</strong><br/>
                    Status: {d.category}<br/>
                    Days Left: {d.days_left}<br/>
                    Seats Remaining: {d.seats_remaining}<br/>
                    Load Factor: {(d.load_factor * 100).toFixed(1)}%
                  </div>
                )
              }}
            />
            <Legend />
            <Scatter name="Critical" data={data.filter(d => d.category === 'Critical')} fill="#ef4444" />
            <Scatter name="Warning" data={data.filter(d => d.category === 'Warning')} fill="#f59e0b" />
            <Scatter name="Safe" data={data.filter(d => d.category === 'Safe')} fill="#10b981" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

function RouteProfitability() {
  const [data, setData] = useState([])

  useEffect(() => {
    axios.get(`${API_BASE}/route_profitability`).then(res => setData(res.data.data)).catch(console.error)
  }, [])

  return (
    <div>
      <header className="header">
        <h1 className="header-title">Route Profitability</h1>
        <p className="header-subtitle">Top 20 most profitable routes across the network.</p>
      </header>

      <div className="card" style={{ height: '500px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 20, right: 30, left: 100, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" tickFormatter={(value) => `₹${value/1000}k`} />
            <YAxis dataKey="route" type="category" width={120} tick={{fontSize: 12}} />
            <Tooltip 
              formatter={(value) => [`₹${value.toLocaleString()}`, 'Total Revenue']}
            />
            <Bar dataKey="revenue" fill="#3b82f6" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.margin > 35 ? '#10b981' : '#3b82f6'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
