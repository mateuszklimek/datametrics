from tasks import send_livecoin_to_graphite, send_stocks_to_graphite
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run manual ingestion of metrics (crypto, stocks or both) to graphite"
    )

    parser.add_argument(
        "--crypto", action="store_true", help="Run ingestion of crypto data"
    )
    parser.add_argument(
        "--stocks", action="store_true", help="Run ingestion of stocks data"
    )

    args = parser.parse_args()

    if not any((args.crypto, args.stocks)):
        print("Specify at least one of --stocks --crypto")

    if args.crypto:
        send_livecoin_to_graphite()
    if args.stocks:
        send_stocks_to_graphite()
