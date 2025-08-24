#!/usr/bin/env python3
import argparse
import os
import pandas as pd
import sys
import re

VALID_TYPES = {"creditoraccount": "creditorAccount", "fourthparty": "fourthParty"}

def normalize_str(x):
    if x is None:
        return ""
    return str(x).strip()

def to_number_or_none(s: str):
    try:
        return float(str(s).strip())
    except Exception:
        return None

def emit_yaml_line(key: str, value: str, indent: int, comment: str = "") -> str:
    # Quote always to preserve formatting
    qv = str(value).replace("'", "''")
    line = f"{' ' * indent}{key}:'{qv}'"
    if comment:
        line += f" #{comment}"
    return line + "\n"

def main():
    home = os.path.expanduser("~")
    default_input = os.path.join(home, "Documents", "input.xlsx")
    default_output = os.path.join(home, "Documents", "output.yaml")
    default_error_report = os.path.join(home, "Documents", "validation_errors.csv")

    ap = argparse.ArgumentParser(description="Convert single-sheet Excel to YAML with validations.")
    ap.add_argument(
        "input_xlsx",
        nargs="?",
        default=default_input,
        help="Excel file path (default: ~/Documents/input.xlsx)",
    )
    ap.add_argument(
        "-o", "--output",
        default=default_output,
        help="Output YAML path (default: ~/Documents/output.yaml)",
    )
    ap.add_argument(
        "--error-report",
        default=None,
        help="Optional CSV path to write detailed row-level errors. Default: <output_dir>/validation_errors.csv",
    )
    # Behavior flags
    ap.add_argument("--dedupe-accounts", action="store_true",
                    help="Drop duplicate accountNumber entries (creditorAccount) keeping first")
    ap.add_argument("--dedupe-nzbn", action="store_true",
                    help="Drop duplicate NZBN entries (fourthParty) keeping first")
    ap.add_argument("--fail-on-duplicate-account", action="store_true",
                    help="Fail if duplicate accountNumbers found")
    ap.add_argument("--fail-on-duplicate-nzbn", action="store_true",
                    help="Fail if duplicate NZBNs found")
    ap.add_argument("--require-numeric-paymentlimit", action="store_true",
                    help="Fail if any paymentLimit is not numeric")
    ap.add_argument("--max-creditor", type=float, default=None,
                    help="Max allowed paymentLimit for creditorAccount rows (inclusive)")
    ap.add_argument("--max-fourth", type=float, default=None,
                    help="Max allowed paymentLimit for fourthParty rows (inclusive)")
    args = ap.parse_args()

    # Resolve default error report path
    if args.error_report:
        error_report_path = args.error_report
    else:
        out_dir = os.path.dirname(os.path.abspath(args.output)) or "."
        error_report_path = os.path.join(out_dir, "validation_errors.csv")

    # Load Excel, preserve original row numbers
    try:
        xls = pd.ExcelFile(args.input_xlsx)
    except Exception as e:
        print(f"ERROR: Could not open Excel file: {e}", file=sys.stderr)
        sys.exit(1)

    if "data" not in xls.sheet_names:
        print("ERROR: Missing required sheet 'data'", file=sys.stderr)
        sys.exit(2)

    df_raw = pd.read_excel(xls, sheet_name="data", dtype=str)
    # Add 1 for 0-index, +1 for header → +2 total
    df_raw["excel_row"] = df_raw.index + 2

    for col in ["type","id","paymentLimit","comment"]:
        if col not in df_raw.columns:
            print(f"ERROR: Missing required column '{col}' in 'data' sheet", file=sys.stderr)
            sys.exit(2)

    # Clean/normalize
    df_raw["type_norm"] = df_raw["type"].map(lambda s: VALID_TYPES.get(normalize_str(s).lower(), ""))
    df_raw["id"] = df_raw["id"].map(lambda s: normalize_str(s))
    df_raw["paymentLimit"] = df_raw["paymentLimit"].map(lambda s: normalize_str(s))
    df_raw["comment"] = df_raw["comment"].map(lambda s: normalize_str(s))

    # Drop fully blank rows (but keep excel_row mapping)
    df = df_raw[~(df_raw[["type_norm","id","paymentLimit","comment"]]
                  .apply(lambda r: all(v=="" for v in r.values), axis=1))].copy()

    # Split by type
    cred = df[df["type_norm"]=="creditorAccount"].copy()
    fourth = df[df["type_norm"]=="fourthParty"].copy()

    # Collect detailed row-level errors
    error_rows = []  # list of dicts: {excel_row, type, id, paymentLimit, reason}

    def add_errors(subdf: pd.DataFrame, reason: str):
        # Append every row in subdf as an error with given reason
        for _, rr in subdf.iterrows():
            error_rows.append({
                "excel_row": int(rr.get("excel_row", -1)),
                "type": rr.get("type_norm") or rr.get("type") or "",
                "id": rr.get("id", ""),
                "paymentLimit": rr.get("paymentLimit", ""),
                "reason": reason
            })

    # Validate types
    bad_type = df[df["type_norm"]==""]
    if len(bad_type) > 0:
        add_errors(bad_type, "invalid 'type' (must be creditorAccount or fourthParty)")

    # NZBN format & duplicates
    if not fourth.empty:
        fourth["nzbn"] = fourth["id"].map(lambda s: re.sub(r"\s+","", s))
        bad_nzbn = fourth[~fourth["nzbn"].str.fullmatch(r"\d{13}", na=False)]
        if len(bad_nzbn) > 0:
            add_errors(bad_nzbn, "invalid NZBN (must be 13 digits)")

        dup_nzbn_mask = fourth.duplicated(subset=["nzbn"], keep=False)
        dup_nzbn = fourth[dup_nzbn_mask]
        if len(dup_nzbn) > 0:
            add_errors(dup_nzbn, "duplicate NZBN")

    # accountNumber duplicates
    if not cred.empty:
        cred["accountNumber"] = cred["id"]
        dup_acct_mask = cred.duplicated(subset=["accountNumber"], keep=False)
        dup_acct = cred[dup_acct_mask]
        if len(dup_acct) > 0:
            add_errors(dup_acct, "duplicate accountNumber")

    # paymentLimit numeric & thresholds
    if args.require_numeric_paymentlimit or args.max_fourth is not None or args.max_creditor is not None:
        if not fourth.empty:
            fourth["_pl_num"] = fourth["paymentLimit"].map(lambda x: to_number_or_none(x))
            if args.require_numeric_paymentlimit:
                bad_num_fourth = fourth[fourth["_pl_num"].isna()]
                if len(bad_num_fourth) > 0:
                    add_errors(bad_num_fourth, "non-numeric paymentLimit")
            if args.max_fourth is not None:
                over = fourth[(~fourth["_pl_num"].isna()) & (fourth["_pl_num"] > args.max_fourth)]
                if len(over) > 0:
                    add_errors(over, f"paymentLimit > {args.max_fourth}")

        if not cred.empty:
            cred["_pl_num"] = cred["paymentLimit"].map(lambda x: to_number_or_none(x))
            if args.require_numeric_paymentlimit:
                bad_num_cred = cred[cred["_pl_num"].isna()]
                if len(bad_num_cred) > 0:
                    add_errors(bad_num_cred, "non-numeric paymentLimit")
            if args.max_creditor is not None:
                overc = cred[(~cred["_pl_num"].isna()) & (cred["_pl_num"] > args.max_creditor)]
                if len(overc) > 0:
                    add_errors(overc, f"paymentLimit > {args.max_creditor}")

    # Summaries (as before)
    errors_summary = []

    # From bad_type
    if len(bad_type) > 0:
        errors_summary.append(f"{len(bad_type)} rows have invalid 'type'.")

    # From NZBN format & duplicates
    if not fourth.empty:
        bad_nzbn_count = len(fourth[~fourth["nzbn"].str.fullmatch(r"\d{13}", na=False)])
        if bad_nzbn_count > 0:
            errors_summary.append(f"{bad_nzbn_count} fourthParty rows have invalid NZBN (must be 13 digits).")
        dup_nzbn_count = int((fourth.duplicated(subset=["nzbn"], keep=False)).sum())
        if dup_nzbn_count > 0:
            errors_summary.append(f"{dup_nzbn_count} fourthParty rows have duplicate NZBNs.")

    # From account duplicates
    if not cred.empty:
        dup_acct_count = int((cred.duplicated(subset=["accountNumber"], keep=False)).sum())
        if dup_acct_count > 0:
            errors_summary.append(f"{dup_acct_count} creditorAccount rows have duplicate accountNumbers.")

    # From numeric/threshold checks
    if (args.require_numeric_paymentlimit or args.max_fourth is not None or args.max_creditor is not None):
        if not fourth.empty and args.require_numeric_paymentlimit:
            bad_num_fourth_count = int(fourth["_pl_num"].isna().sum())
            if bad_num_fourth_count > 0:
                errors_summary.append(f"{bad_num_fourth_count} fourthParty rows have non-numeric paymentLimit.")
        if not cred.empty and args.require_numeric_paymentlimit:
            bad_num_cred_count = int(cred["_pl_num"].isna().sum())
            if bad_num_cred_count > 0:
                errors_summary.append(f"{bad_num_cred_count} creditorAccount rows have non-numeric paymentLimit.")
        if not fourth.empty and args.max_fourth is not None:
            over_fp_count = int(((~fourth["_pl_num"].isna()) & (fourth["_pl_num"] > args.max_fourth)).sum())
            if over_fp_count > 0:
                errors_summary.append(f"{over_fp_count} fourthParty rows have paymentLimit > {args.max_fourth}.")
        if not cred.empty and args.max_creditor is not None:
            over_cred_count = int(((~cred["_pl_num"].isna()) & (cred["_pl_num"] > args.max_creditor)).sum())
            if over_cred_count > 0:
                errors_summary.append(f"{over_cred_count} creditorAccount rows have paymentLimit > {args.max_creditor}.")

    # If any error, print summary + detailed list and write CSV, then exit
    if error_rows:
        print("VALIDATION FAILED:", file=sys.stderr)
        for s in errors_summary:
            print(f" - {s}", file=sys.stderr)

        # Sort detailed rows by excel_row then reason
        error_rows_sorted = sorted(error_rows, key=lambda r: (r["excel_row"], r["reason"]))

        # Print detailed lines
        for er in error_rows_sorted:
            print(
                f"Row {er['excel_row']}: {er['type']} — {er['reason']} — id={er['id']} paymentLimit={er['paymentLimit']}",
                file=sys.stderr
            )

        # Write CSV report
        try:
            pd.DataFrame(error_rows_sorted).to_csv(error_report_path, index=False)
            print(f"\nDetailed error report written to: {error_report_path}", file=sys.stderr)
        except Exception as e:
            print(f"\nWARNING: Could not write error report CSV: {e}", file=sys.stderr)

        sys.exit(3)

    # Optional de-dupe (only runs when there are no errors)
    # (If you want dedupe to happen even with warnings, move dedupe above, but keep validation before)
    if args.dedupe_nzbn and not fourth.empty:
        fourth = fourth.drop_duplicates(subset=["nzbn"], keep="first")
    if args.dedupe_accounts and not cred.empty:
        cred = cred.drop_duplicates(subset=["accountNumber"], keep="first")

    # Emit YAML
    lines = []
    lines.append("creditorAccounts:\n")
    for _, r in cred.iterrows():
        acct = r["accountNumber"]
        pl = r["paymentLimit"]
        cmt = r["comment"]
        if not acct:
            continue
        lines.append("  - " + emit_yaml_line("accountNumber", acct, 4).lstrip())
        lines.append(emit_yaml_line("paymentLimit", pl, 6, cmt))

    lines.append("fourthParties:\n")
    for _, r in fourth.iterrows():
        nzbn = r["nzbn"]
        pl = r["paymentLimit"]
        cmt = r["comment"]
        if not nzbn:
            continue
        lines.append("  - " + emit_yaml_line("nzbn", nzbn, 4).lstrip())
        lines.append(emit_yaml_line("paymentLimit", pl, 6, cmt))

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("".join(lines))

    print(f"Wrote YAML to {args.output}")

if __name__ == "__main__":
    main()
