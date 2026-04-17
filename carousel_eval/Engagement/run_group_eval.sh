#!/bin/bash
# Run evaluation for top and bottom consumer groups.
# Usage: bash run_group_eval.sh <order_history.csv>
#
# Prerequisites:
#   - carousels_top.csv and carousels_bottom.csv in this directory
#   - Order history CSV with columns: CONSUMER_ID, DAY_PART, ITEM_ID, ITEM_NAME, DESCRIPTION, CUISINE_TAGS_FROM_MENU

set -e

ORDER_CSV="${1:?Usage: bash run_group_eval.sh <order_history.csv>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EVAL_SCRIPT="$SCRIPT_DIR/../local_eval_test.py"
OUTPUT_DIR="$SCRIPT_DIR/results"

mkdir -p "$OUTPUT_DIR"

echo "=== Evaluating TOP group (highest converters) ==="
python "$EVAL_SCRIPT" \
  --carousel_csv "$SCRIPT_DIR/carousels_top.csv" \
  --order_history_csv "$ORDER_CSV" \
  --source_name top \
  --embed_mode title_metadata \
  --output_dir "$OUTPUT_DIR"

echo ""
echo "=== Evaluating BOTTOM group (zero converters) ==="
python "$EVAL_SCRIPT" \
  --carousel_csv "$SCRIPT_DIR/carousels_bottom.csv" \
  --order_history_csv "$ORDER_CSV" \
  --source_name bottom \
  --embed_mode title_metadata \
  --output_dir "$OUTPUT_DIR"

echo ""
echo "=== Done. Results in $OUTPUT_DIR ==="
echo "  eval_top.csv"
echo "  eval_bottom.csv"
