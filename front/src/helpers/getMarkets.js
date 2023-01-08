export const getMarkets = async () => {

    // console.log('Entro')
  
    // const url = 'http://127.0.0.1:1234/api/open-markets'
    const url = `${tradinbBotApi}/api/open-markets`
    const resp = await fetch(url)
    const data = await resp.json();
  
    // console.log(data.open_markets, 'data.open_markets')
  
    const open_markets = data.open_markets.map(
      (market) => {
        return {
          id: market.market,
          name: market.market,
          operating: market.operating
        }
      }
    )
  
    // console.log(open_markets, 'open_markets')
  
    // setMarkets(data.open_markets)
  
    // console.log(data, 'data')
    return open_markets;
  }