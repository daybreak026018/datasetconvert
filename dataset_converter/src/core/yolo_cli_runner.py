"""
Small subprocess entrypoint for YOLO train and predict jobs.
"""

from __future__ import annotations

import argparse
import sys


def _load_yolo():
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise RuntimeError(
            "未能导入 ultralytics，请先执行: python -m pip install -U ultralytics"
        ) from exc
    return YOLO


def run_train(args):
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
