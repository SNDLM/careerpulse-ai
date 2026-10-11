"""Periodically refresh Madrid job offers from Adzuna."""

import logging
import time

from careerpulse.pipeline import run_adzuna_etl

LOGGER = logging.getLogger(__name__)
REFRESH_SECONDS = 24 * 60 * 60
RETRY_SECONDS = 5 * 60


def main() -> None:
    """Fetch jobs now and repeat every 24 hours."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    while True:
        try:
            count = run_adzuna_etl(
                what="data",
                where="Madrid",
                results_per_page=20,
            )
        except Exception:
            LOGGER.exception("Job refresh failed; retrying in 5 minutes.")
            time.sleep(RETRY_SECONDS)
        else:
            LOGGER.info("Processed %s Adzuna jobs.", count)
            time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    main()