export const operateMarket = async (market, money) => {

    console.log(money)

    const url = 'http://127.0.0.1:1234/api/trade'
    const resp = await fetch(url,
        {
            method: 'POST',
            body: JSON.stringify(
                {
                    'market': market, 
                    'money': money
                }
            )
        }
    )
    const data = await resp.json();

}