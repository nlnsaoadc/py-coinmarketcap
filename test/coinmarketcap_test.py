from unittest import TestCase, mock

from coinmarketcap.coinmarketcap import CoinMarketCap, KeyTypeError


class CoinMarketCapTestCase(TestCase):
    def setUp(self):
        self.api = CoinMarketCap(key="123test", key_type="enterprise")
        self.api_basic = CoinMarketCap(key="123test", key_type="basic")
        self.api_hobbyist = CoinMarketCap(key="123test", key_type="hobbyist")
        self.api_startup = CoinMarketCap(key="123test", key_type="startup")
        self.api_standard = CoinMarketCap(key="123test", key_type="standard")
        self.api_professional = CoinMarketCap(
            key="123test", key_type="professional"
        )
        self.api_enterprise = CoinMarketCap(
            key="123test", key_type="enterprise"
        )

    def test_get_headers(self):
        headers = self.api._get_headers()
        self.assertIsNotNone(headers["Accept"])
        self.assertIsNotNone(headers["X-CMC_PRO_API_KEY"])

    @mock.patch(
        "requests.get", return_value=mock.Mock(status_code=200, json=lambda: {})
    )
    def test_get(self, mock_get):
        self.api._get("test")
        mock_get.assert_called_once_with(
            url="https://pro-api.coinmarketcap.com/test",
            headers={
                "Accept": "application/json",
                "X-CMC_PRO_API_KEY": "123test",
            },
            params=None,
        )

    @mock.patch("coinmarketcap.coinmarketcap.logger.warning")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=lambda: {"message": "Not Found"},
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status(self, mock_get, mock_log):
        with self.assertRaises(Exception) as context:
            self.api._get("test")
        self.assertEqual(
            "404 404 Not Found Message",
            str(context.exception),
        )
        mock_log.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap.logger.info")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=mock.Mock(side_effect=Exception("")),
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status_fail_silently(self, mock_get, mock_log):
        self.api.fail_silently = True
        self.assertEqual(self.api._get("test"), None)
        mock_log.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap.logger.error")
    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_wrong_key_type_str(self, mock_get, mock_log):
        try:
            self.api_basic.get_trending_latest()
        except KeyTypeError as error:
            self.assertEqual(type(str(error)), str)

    @mock.patch("coinmarketcap.coinmarketcap.logger.error")
    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_requires_startup(self, mock_get, mock_log):
        with self.assertRaises(KeyTypeError):
            self.api_basic.get_trending_latest()
        self.api_startup.get_trending_latest()
        mock_log.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap.logger.error")
    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_requires_standard(self, mock_get, mock_log):
        with self.assertRaises(KeyTypeError):
            self.api_basic.get_exchange_quotes_latest()
        self.api_standard.get_exchange_quotes_latest()
        mock_log.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap.logger.error")
    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_requires_enterprise(self, mock_get, mock_log):
        with self.assertRaises(KeyTypeError):
            self.api_basic.get_blockchain_statistics_latest()
        self.api_enterprise.get_blockchain_statistics_latest()
        mock_log.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_airdrop(self, mock_get):
        self.api.get_airdrop(id="")
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_airdrops(self, mock_get):
        self.api.get_airdrops()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_categories(self, mock_get):
        self.api.get_categories()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_category(self, mock_get):
        self.api.get_category(id="")
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_info(self, mock_get):
        self.api.get_info(id=[""])
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_map(self, mock_get):
        self.api.get_map(sort="cmc_rank")
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_listings_historical(self, mock_get):
        self.api.get_listings_historical(date="")
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_listings_latest(self, mock_get):
        self.api.get_listings_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_market_pairs_latest(self, mock_get):
        self.api.get_market_pairs_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_ohlcv_historical(self, mock_get):
        self.api.get_ohlcv_historical()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_ohlcv_latest(self, mock_get):
        self.api.get_ohlcv_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_price_performance_stats_latest(self, mock_get):
        self.api.get_price_performance_stats_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_quotes_historical(self, mock_get):
        self.api.get_quotes_historical()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_quotes_latest(self, mock_get):
        self.api.get_quotes_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_trending_gainers_losers(self, mock_get):
        self.api.get_trending_gainers_losers()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_trending_latest(self, mock_get):
        self.api.get_trending_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_trending_most_visited(self, mock_get):
        self.api.get_trending_most_visited()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_fiat_map(self, mock_get):
        self.api.get_fiat_map()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_exchange_info(self, mock_get):
        self.api.get_exchange_info()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_exchange_map(self, mock_get):
        self.api.get_exchange_map()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_exchange_listings_latest(self, mock_get):
        self.api.get_exchange_listings_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_exchange_market_pairs_latest(self, mock_get):
        self.api.get_exchange_market_pairs_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_exchange_quotes_historical(self, mock_get):
        self.api.get_exchange_quotes_historical()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_exchange_quotes_latest(self, mock_get):
        self.api.get_exchange_quotes_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_global_metrics_quotes_historical(self, mock_get):
        self.api.get_global_metrics_quotes_historical()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_global_metrics_quotes_latest(self, mock_get):
        self.api.get_global_metrics_quotes_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_tools_price_conversion(self, mock_get):
        self.api.get_tools_price_conversion(amount=1.0)
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_blockchain_statistics_latest(self, mock_get):
        self.api.get_blockchain_statistics_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_partners_flipside_crypto_fcas_listings_latest(self, mock_get):
        self.api.get_partners_flipside_crypto_fcas_listings_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_partners_flipside_crypto_fcas_quotes_latest(self, mock_get):
        self.api.get_partners_flipside_crypto_fcas_quotes_latest()
        mock_get.assert_called_once()

    @mock.patch("coinmarketcap.coinmarketcap" ".CoinMarketCap._get")
    def test_get_key_info(self, mock_get):
        self.api.get_key_info()
        mock_get.assert_called_once()
