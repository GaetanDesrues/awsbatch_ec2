import os
# import logging
# import gatools as ga


def main():
    print("In Job")
    print("INPUT_FILE:", os.getenv("INPUT_FILE"))
    print("OUTPUT_BUCKET:", os.getenv("OUTPUT_BUCKET"))
    print("JOB_NAME:", os.getenv("JOB_NAME"))


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # log = ga.get_logger()

    main()
