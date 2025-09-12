import { useState, useEffect } from 'react'
import MarketOverview from './components/dashboard/MarketOverview';  // Works with .jsx files
import './App.css'

function App() {
  const [coinPrices, setCoinPrices] = useState({})
  const [loading, setLoading] = useState(true)

  const coins = [
    { id: 'bitcoin', name: 'Bitcoin', symbol: 'BTC' },
    { id: 'ethereum', name: 'Ethereum', symbol: 'ETH' },
    { id: 'solana', name: 'Solana', symbol: 'SOL' },
    { id: 'sui', name: 'Sui', symbol: 'SUI' },
    { id: 'ripple', name: 'XRP', symbol: 'XRP' }
  ]

  useEffect(() => {
    const coinIds = coins.map(coin => coin.id).join(',')
    
    fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${coinIds}&vs_currencies=usd&include_24hr_change=true`)
      .then(response => response.json())
      .then(data => {
        setCoinPrices(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching coin prices:', error)
        setLoading(false)
      })
  }, [])

  return (
    <div className="App">
      <h1>Crypto Portfolio Dashboard</h1>
      
      {loading ? (
        <p>Loading coin prices...</p>
      ) : (
        <div className="coins-grid">
          {coins.map(coin => (
            <div key={coin.id} className="coin-card">
              <h3>{coin.name} ({coin.symbol})</h3>
              <p className="price">
                ${coinPrices[coin.id]?.usd?.toLocaleString()}
              </p>
              <p className={`change ${coinPrices[coin.id]?.usd_24h_change >= 0 ? 'positive' : 'negative'}`}>
                24h: {coinPrices[coin.id]?.usd_24h_change?.toFixed(2)}%
              </p>
            </div>
          ))}
        </div>

      )}
      
      {/* NEW: Your MarketOverview component */}
      <MarketOverview />
    </div>
  )
}

export default App

