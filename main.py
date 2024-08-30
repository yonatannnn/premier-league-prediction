from scraper.bettingtips_scraper import BettingTipsScraper
from scraper.sportsgambler_scraper import SportsManGambler
from scraper.sportytrader_scraper import SportyTrader
from data_analysis.analysis import Analysis
from data import predictions1, predictions2, predictions3

def main():
    try:
        with SportyTrader() as trader:
            trader.get_predictions()
    except Exception as e:
        print(f"Error with SportyTrader scraper: {e}")

    try:
        with SportsManGambler() as gambler:
            gambler.get_predictions()
    except Exception as e:
        print(f"Error with SportsManGambler scraper: {e}")

    try:
        with BettingTipsScraper() as betting_tips:
            betting_tips.get_predictions()
    except Exception as e:
        print(f"Error with BettingTipsScraper scraper: {e}")

    try:
        analysis = Analysis(predictions1=predictions1, predictions2=predictions2, predictions3=predictions3)
        analysis.print()
    except Exception as e:
        print(f"Error in analysis: {e}")


if __name__ == "__main__":
    main()
