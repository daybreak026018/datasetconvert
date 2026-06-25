"""
Small subprocess entrypoint for YOLO train and predict jobs.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


def _install_safe_weight_writer():
    """Save best weights as snapshots instead of overwriting best.pt on Windows."""
    original_write_bytes = Path.write_bytes
    best_save_counts = {}

    def snapshot_path(path):
        key = str(path)
        best_save_counts[key] = best_save_counts.get(key, 0) + 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return path.with_name(f"best_{timestamp}_{best_save_counts[key]:03d}{path.suffix}")

    def safe_write_bytes(path, data):
        if path.suffix.lower() == ".pt" and path.name.lower() == "best.pt":
            target = snapshot_path(path)
            original_write_bytes(target, data)
            print(f"[DataForge] best 权重已按快照保存，不覆盖 best.pt: {target}", flush=True)
            return len(data)

        try:
            return original_write_bytes(path, data)
        except OSError as exc:
            if path.suffix.lower() != ".pt":
                raise

            fallback_path = path.with_name(
                f"{path.stem}_fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
            )
            original_write_bytes(fallback_path, data)
            print(
                f"[DataForge] 权重覆盖失败，已另存为: {fallback_path}。原错误: {exc}",
                flush=True,
            )
            return len(data)

    Path.write_bytes = safe_write_bytes


def _load_yolo():
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise RuntimeError(
            "未能导入 ultralytics，请先执行: python -m pip install -U ultralytics"
        ) from exc
    return YOLO


def run_train(args):
    _install_safe_weight_writer()
    YOLO = _load_yolo()
    model = YOLO(args.model)
    device = None if args.device == "auto" else args.device
    kwargs = {
        "data": args.data,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": device,
        "project": args.project,
        "name": args.name,
        "workers": args.workers,
        "patience": args.patience,
        "task": args.task,
        "exist_ok": False,
    }
    if args.resume:
        kwargs["resume"] = True
    model.train(**kwargs)


def run_predict(args):
    YOLO = _load_yolo()
    model = YOLO(args.model)
    device = None if args.device == "auto" else args.device
    model.predict(
        source=args.source,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
        device=device,
        project=args.project,
        name=args.name,
        save=True,
        save_txt=args.save_txt,
        save_conf=args.save_conf,
        task=args.task,
    )


def build_parser():
    parser = argparse.ArgumentParser(description="DataForge YOLO runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train = subparsers.add_parser("train")
    train.add_argument("--task", required=True)
    train.add_argument("--model", required=True)
    train.add_argument("--data", required=True)
    train.add_argument("--epochs", type=int, required=True)
    train.add_argument("--imgsz", type=int, required=True)
    train.add_argument("--batch", type=int, required=True)
    train.add_argument("--device", required=True)
    train.add_argument("--project", required=True)
    train.add_argument("--name", required=True)
    train.add_argument("--workers", type=int, required=True)
    train.add_argument("--patience", type=int, required=True)
    train.add_argument("--resume", action="store_true")
    train.set_defaults(func=run_train)

    predict = subparsers.add_parser("predict")
    predict.add_argument("--task", required=True)
    predict.add_argument("--model", required=True)
    predict.add_argument("--source", required=True)
    predict.add_argument("--conf", type=float, required=True)
    predict.add_argument("--iou", type=float, required=True)
    predict.add_argument("--imgsz", type=int, required=True)
    predict.add_argument("--device", required=True)
    predict.add_argument("--project", required=True)
    predict.add_argument("--name", default="predict")
    predict.add_argument("--save-txt", action="store_true")
    predict.add_argument("--save-conf", action="store_true")
    predict.set_defaults(func=run_predict)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])

