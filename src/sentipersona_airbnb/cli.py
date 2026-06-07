from __future__ import annotations

import argparse
from collections.abc import Callable

from .clustering import run_regional_clustering
from .config import load_config, standard_files, standard_paths
from .data import preprocess_inside_airbnb, validate_occupancy_proxy
from .download import download_fasttext_lid, download_inside_airbnb
from .evaluation import run_evaluation
from .modeling import encode_airbnb_reviews, evaluate_sentiment_encoder, train_senticse
from .persona import generate_regional_personas
from .sentiment import label_airbnb_sentiment
from .timeseries import run_timeseries
from .utils import ensure_dirs, read_json, seed_everything, setup_logging, write_json


def load_and_prepare(args: argparse.Namespace) -> dict:
    cfg = load_config(args.config)
    seed_everything(int(cfg["experiment"]["seed"]))
    return cfg


def cmd_init(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    paths = standard_paths(cfg)
    ensure_dirs(paths.values())
    write_json(
        {"paths": {key: str(value) for key, value in paths.items()}},
        paths["reports_dir"] / "paths.json",
    )
    print("Initialized experiment directories.")


def cmd_download(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    ran = False
    if args.inside_airbnb or args.all:
        print(download_inside_airbnb(cfg))
        ran = True
    if args.fasttext or args.all:
        print(download_fasttext_lid(cfg))
        ran = True
    if not ran:
        raise SystemExit("Select --inside-airbnb, --fasttext, or --all.")


def cmd_label_airbnb_sentiment(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(label_airbnb_sentiment(cfg))


def cmd_preprocess_airbnb(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    outputs = preprocess_inside_airbnb(cfg)
    print(outputs)


def run_occupancy_validation(cfg: dict) -> dict:
    import pandas as pd

    paths = standard_paths(cfg)
    files = standard_files(cfg)
    calendar_occ = pd.read_parquet(files["monthly_occupancy"])
    review_occ = pd.read_parquet(files["review_based_occupancy"])
    result = validate_occupancy_proxy(
        calendar_occ,
        review_occ,
        float(cfg["occupancy"]["min_calendar_review_correlation"]),
    )
    write_json(result, paths["reports_dir"] / "occupancy_proxy_validation.json")
    return result


def cmd_validate_occupancy(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    result = run_occupancy_validation(cfg)
    print(result)


def cmd_train(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(train_senticse(cfg))


def cmd_evaluate_sentiment_encoder(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(evaluate_sentiment_encoder(cfg))


def cmd_embed(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(encode_airbnb_reviews(cfg))


def cmd_cluster(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(run_regional_clustering(cfg))


def cmd_personas(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(generate_regional_personas(cfg))


def cmd_timeseries(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(run_timeseries(cfg))


def cmd_evaluate(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    print(run_evaluation(cfg))


def cmd_report(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    paths = standard_paths(cfg)
    report_files = sorted(paths["reports_dir"].glob("*.json"))
    for path in report_files:
        print(f"\n## {path.name}")
        print(read_json(path))


def cmd_run_all(args: argparse.Namespace) -> None:
    cfg = load_and_prepare(args)
    paths = standard_paths(cfg)
    ensure_dirs(paths.values())

    steps: list[tuple[str, Callable[[dict], object]]] = [
        ("download_inside_airbnb", download_inside_airbnb),
        ("download_fasttext_lid", download_fasttext_lid),
        ("preprocess_inside_airbnb", preprocess_inside_airbnb),
        ("validate_occupancy_proxy", run_occupancy_validation),
        ("label_airbnb_sentiment", label_airbnb_sentiment),
        ("train_senticse", train_senticse),
        ("evaluate_sentiment_encoder", evaluate_sentiment_encoder),
        ("encode_airbnb_reviews", encode_airbnb_reviews),
        ("run_regional_clustering", run_regional_clustering),
        ("generate_regional_personas", generate_regional_personas),
        ("run_timeseries", run_timeseries),
        ("run_evaluation", run_evaluation),
    ]
    outputs = {}
    for name, func in steps:
        print(f"=== {name} ===")
        outputs[name] = func(cfg)
        print(outputs[name])
    write_json(outputs, paths["reports_dir"] / "run_all_outputs.json")


def add_config_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-c",
        "--config",
        default="configs/experiment.example.yaml",
        help="Path to YAML experiment config.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentipersona",
        description="Run the SentiPersona-Airbnb experiment pipeline.",
    )
    parser.add_argument("--log-level", default="INFO")
    sub = parser.add_subparsers(dest="command", required=True)

    commands: list[tuple[str, Callable[[argparse.Namespace], None], str]] = [
        ("init", cmd_init, "Create experiment directories."),
        ("preprocess-airbnb", cmd_preprocess_airbnb, "Clean Airbnb reviews and occupancy data."),
        (
            "label-airbnb-sentiment",
            cmd_label_airbnb_sentiment,
            "Pseudo-label Airbnb reviews with binary sentiment for fine-tuning.",
        ),
        (
            "validate-occupancy",
            cmd_validate_occupancy,
            "Validate calendar occupancy against review proxy.",
        ),
        ("train", cmd_train, "Fine-tune the SentiCSE encoder."),
        (
            "evaluate-sentiment-encoder",
            cmd_evaluate_sentiment_encoder,
            "Evaluate base vs fine-tuned sentiment embedding separation.",
        ),
        ("embed", cmd_embed, "Encode cleaned Airbnb reviews."),
        ("cluster", cmd_cluster, "Run regional UMAP/HDBSCAN clustering."),
        ("personas", cmd_personas, "Generate LLM persona definitions."),
        ("timeseries", cmd_timeseries, "Build monthly persona and analysis datasets."),
        ("evaluate", cmd_evaluate, "Run statistical and predictive evaluations."),
        ("report", cmd_report, "Print JSON reports."),
        ("run-all", cmd_run_all, "Run the full pipeline end to end."),
    ]
    for name, func, help_text in commands:
        child = sub.add_parser(name, help=help_text)
        add_config_arg(child)
        child.set_defaults(func=func)

    download = sub.add_parser("download", help="Download data/model files.")
    add_config_arg(download)
    download.add_argument("--inside-airbnb", action="store_true")
    download.add_argument("--fasttext", action="store_true")
    download.add_argument("--all", action="store_true")
    download.set_defaults(func=cmd_download)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(args.log_level)
    args.func(args)


if __name__ == "__main__":
    main()
