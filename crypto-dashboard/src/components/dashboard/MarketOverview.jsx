import { useState, useEffect } from 'react';

function MarketOverview() {
  // State for our market data (starts empty, will be filled by agents later)
  const [marketData, setMarketData] = useState({
    fearGreedIndex: null,
    btcDominance: null,
    loading: true
  });

  // Simulate data fetching (Week 2 will replace this with real agent data)
  useEffect(() => {
    // Mock data for now - our agents will provide real data
    setTimeout(() => {
      setMarketData({
        fearGreedIndex: { value: 45, state: 'Neutral' },
        btcDominance: { value: 54.2, change24h: -1.3 },
        loading: false
      });
    }, 1500);
  }, []);

  return (
    <div className="market-overview">
      <h2>Market Overview</h2>
      
      {marketData.loading ? (
        <p>Loading market data...</p>
      ) : (
        <div>
          <div className="metric">
            <strong>Fear & Greed Index:</strong> {marketData.fearGreedIndex.value} ({marketData.fearGreedIndex.state})
            <br />
            <small>Market sentiment appears {marketData.fearGreedIndex.state.toLowerCase()}</small>
          </div>
          
          <div className="metric">
            <strong>BTC Dominance:</strong> {marketData.btcDominance.value}% ({marketData.btcDominance.change24h > 0 ? '+' : ''}{marketData.btcDominance.change24h}%)
            <br />
            <small>Bitcoin's share of crypto market cap</small>
          </div>
        </div>
      )}
    </div>
  );
}

export default MarketOverview;