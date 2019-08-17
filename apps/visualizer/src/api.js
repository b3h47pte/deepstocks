const rp = require('request-promise-native');

export function getHistoricalStockEodInfo(symbol) {
    return rp({
        uri: 'http://127.0.0.1:5000/eodInfo',
        qs: {
            'inp': symbol
        },
        json: true
    }).then(function(body){
        return body;
    });
}
