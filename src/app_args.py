import argparse


class Args:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="California Ballot Propositions CLI"
        )
        self.parser.add_argument(
            "propositions_json",
            type=str,
            help="Path to the propositions JSON file (e.g. src/compiled_propositions.json)",
        )
        self.parser.add_argument(
            "-m",
            "--model",
            type=str,
            default="gpt-4o",
            help="Specify the model to use (default: gpt-4o)",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            type=str,
            default="./out/compiled_prop_results.json",
            help="Specify the output file (e.g. ./out/compiled_prop_results.json)",
        )

    def parse(self):
        return self.parser.parse_args()
