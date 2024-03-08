import aiohttp


async def wb_response(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()


async def wb_api(nm: str = '178601980'):
    url = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-2228342&spp=27&nm={nm}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                json = await response.json()
                summ = 0
                for size in json['data']['products'][0]['sizes']:
                    for stock in size['stocks']:
                        summ += stock['qty']
                return {
                    'name': json['data']['products'][0]['name'],
                    'id': json['data']['products'][0]['id'],
                    'salePriceU': json['data']['products'][0]['salePriceU'],
                    'supplierRating': json['data']['products'][0]['supplierRating'],
                    'stocks': summ
                }
