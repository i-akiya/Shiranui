import argparse
from .server import mcp


def main():
    """CDISC Library Retriever: A tool to retrieve the metadata from the CDISC Library."""
    parser = argparse.ArgumentParser(
        description="Give you the ability to retrieve the metadata from the CDISC Library.",
    )
    parser.parse_args()
    mcp.run()


if __name__ == "__main__":
    main()
