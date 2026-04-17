"""
Compute ILD (Intra-List Diversity) for sparse_cx prompt variants using only TITLE embeddings.

Usage:
    python carousel_eval/sparse_cx/eval_title_ild.py
"""

import os

import numpy as np
import pandas as pd


def intra_list_diversity(carousel_embs: np.ndarray):
    """ILD = 1 - mean pairwise cosine similarity (unit-normed inputs)."""
    k = len(carousel_embs)
    if k < 2:
        return None
    sim = carousel_embs @ carousel_embs.T
    i, j = np.triu_indices(k, k=1)
    return float(1.0 - sim[i, j].mean())

SPARSE_DIR = os.path.dirname(__file__)
PROMPT_FILES = [f"Carousel_evals_prompt{i}.csv" for i in range(1, 5)]


def load_and_normalize(path: str) -> pd.DataFrame:
    """Read a sparse_cx CSV and normalize to standard schema."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"daypart": "day_part", "rank": "carousel_rank"})
    return df[["consumer_id", "day_part", "carousel_rank", "title"]]


def embed_titles(model, df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    texts = df["title"].fillna("").tolist()
    embs = model.encode(
        texts, batch_size=512, normalize_embeddings=True, show_progress_bar=True
    )
    df["title_emb"] = list(embs)
    return df


def compute_ild_per_group(df: pd.DataFrame) -> pd.DataFrame:
    """Compute ILD for each (consumer_id, day_part) group."""
    results = []
    for (cid, dp), grp in df.groupby(["consumer_id", "day_part"]):
        embs = np.stack(grp["title_emb"].tolist())
        ild = intra_list_diversity(embs)
        results.append({
            "consumer_id": cid,
            "day_part": dp,
            "n_carousels": len(grp),
            "ild": ild,
        })
    return pd.DataFrame(results)


def main():
    from sentence_transformers import SentenceTransformer

    print("[model] Loading all-MiniLM-L6-v2 ...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    all_summaries = []

    for fname in PROMPT_FILES:
        path = os.path.join(SPARSE_DIR, fname)
        prompt_name = fname.replace("Carousel_evals_", "").replace(".csv", "")
        print(f"\n{'='*60}")
        print(f"  {prompt_name}")
        print(f"{'='*60}")

        df = load_and_normalize(path)
        print(f"  Rows: {len(df):,}, Consumers: {df['consumer_id'].nunique()}, "
              f"Dayparts: {df['day_part'].nunique()}")

        df = embed_titles(model, df)
        ild_df = compute_ild_per_group(df)

        # Overall stats
        mean_ild = ild_df["ild"].mean()
        std_ild = ild_df["ild"].std()
        print(f"\n  Overall ILD: {mean_ild:.4f} +/- {std_ild:.4f}  (n={len(ild_df)})")

        # Per-daypart breakdown
        print(f"\n  {'daypart':<24s} | {'count':>5s} | {'ILD mean':>10s} | {'ILD std':>10s}")
        print("  " + "-" * 60)
        for dp in sorted(ild_df["day_part"].unique()):
            grp = ild_df[ild_df["day_part"] == dp]
            print(f"  {dp:<24s} | {len(grp):>5d} | {grp['ild'].mean():>10.4f} | {grp['ild'].std():>10.4f}")

        # Save per-group results
        out_path = os.path.join(SPARSE_DIR, f"ild_{prompt_name}.csv")
        ild_df.to_csv(out_path, index=False)
        print(f"\n  Saved {out_path}")

        all_summaries.append({
            "prompt": prompt_name,
            "n_consumers": df["consumer_id"].nunique(),
            "n_groups": len(ild_df),
            "ild_mean": mean_ild,
            "ild_std": std_ild,
        })

    # Comparison table
    summary_df = pd.DataFrame(all_summaries)
    print(f"\n{'='*60}")
    print("  ILD Comparison Across Prompts")
    print(f"{'='*60}")
    print(summary_df.to_string(index=False))

    summary_path = os.path.join(SPARSE_DIR, "ild_comparison.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"\n[done] Saved {summary_path}")


if __name__ == "__main__":
    main()
