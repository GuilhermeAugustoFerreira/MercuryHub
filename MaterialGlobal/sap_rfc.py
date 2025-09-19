"""
Lightweight SAP RFC helpers for reading tables with RFC_READ_TABLE.

- Uses environment variables for SAP credentials by default.
- Provides a paginated `read_table` to avoid size limits.
- Includes an example `fetch_material_groups_with_texts` for T023/T023T.

Environment variables used (fallbacks can be passed as function args):
  SAP_ASHOST, SAP_SYSNR, SAP_CLIENT, SAP_USER, SAP_PASSWD, SAP_LANG
"""

from __future__ import annotations

import os
from typing import Dict, Iterable, List, Mapping, Optional


def _import_connection():
    try:
        from pyrfc import Connection  # type: ignore
        return Connection
    except Exception as exc:  # pragma: no cover
        raise ImportError(
            "pyrfc is not installed or SAP NW RFC SDK not available. "
            "Install pyrfc and ensure SAP NW RFC SDK is set up."
        ) from exc


def get_connection(
    ashost: Optional[str] = None,
    sysnr: Optional[str] = None,
    client: Optional[str] = None,
    user: Optional[str] = None,
    passwd: Optional[str] = None,
    lang: Optional[str] = None,
):
    """Create a pyrfc Connection from args or environment variables.

    Reads missing params from environment variables: SAP_ASHOST, SAP_SYSNR,
    SAP_CLIENT, SAP_USER, SAP_PASSWD, SAP_LANG.
    """
    Connection = _import_connection()

    params = {
        "ashost": ashost or os.getenv("SAP_ASHOST"),
        "sysnr": sysnr or os.getenv("SAP_SYSNR"),
        "client": client or os.getenv("SAP_CLIENT"),
        "user": user or os.getenv("SAP_USER"),
        "passwd": passwd or os.getenv("SAP_PASSWD"),
        "lang": (lang or os.getenv("SAP_LANG") or "EN"),
    }
    missing = [k for k, v in params.items() if not v]
    if missing:
        raise ValueError(f"Missing SAP RFC parameters: {', '.join(missing)}")

    return Connection(**params)  # type: ignore[arg-type]


def read_table(
    tablename: str,
    fields: Optional[Iterable[str]] = None,
    where: Optional[Iterable[str]] = None,
    rowcount: int = 0,
    rowskips: int = 0,
    delimiter: str = "|",
    page_size: int = 1000,
    connection=None,
) -> List[Dict[str, str]]:
    """Read from an SAP table via RFC_READ_TABLE.

    - If `rowcount` is 0, fetches all rows using pagination.
    - Use `where` as an iterable of OPTION lines (<= 72 chars each).
    - Returns a list of dict rows with string values.
    """
    should_close = False
    if connection is None:
        connection = get_connection()
        should_close = True

    try:
        def _call(limit: int, skip: int):
            params: Dict[str, object] = {
                "QUERY_TABLE": tablename,
                "DELIMITER": delimiter,
            }
            if fields:
                params["FIELDS"] = [{"FIELDNAME": f} for f in fields]
            if where:
                params["OPTIONS"] = [{"TEXT": line} for line in where]
            if limit:
                params["ROWCOUNT"] = int(limit)
            if skip:
                params["ROWSKIPS"] = int(skip)
            return connection.call("RFC_READ_TABLE", **params)

        all_rows: List[Dict[str, str]] = []

        if rowcount and rowcount > 0:
            res = _call(rowcount, rowskips)
            cols = [f["FIELDNAME"] for f in res.get("FIELDS", [])]
            for r in res.get("DATA", []):
                all_rows.append(dict(zip(cols, r["WA"].split(delimiter))))
            return all_rows

        # Fetch all rows in pages
        skip = rowskips
        while True:
            res = _call(page_size, skip)
            data = res.get("DATA", [])
            if not data:
                break
            cols = [f["FIELDNAME"] for f in res.get("FIELDS", [])]
            for r in data:
                all_rows.append(dict(zip(cols, r["WA"].split(delimiter))))
            # Safety: stop if less than requested (end reached)
            if len(data) < page_size:
                break
            skip += page_size

        return all_rows
    finally:
        if should_close:
            try:
                connection.close()  # type: ignore[attr-defined]
            except Exception:
                pass


def fetch_material_groups_with_texts(
    langs: Iterable[str] = ("P", "E"),
    connection=None,
) -> Mapping[str, Dict[str, object]]:
    """Fetch T023 (material groups) with language texts from T023T.

    Returns mapping:
      { MATKL: { "SPART": "..", "texts": { lang: text, ... } } }
    """
    # Base groups
    t023 = read_table("T023", fields=["MATKL", "SPART"], connection=connection)

    # Texts for requested languages
    where: List[str] = []
    for i, l in enumerate(langs):
        if i > 0:
            where.append("OR SPRAS = '{}'".format(l))
        else:
            where.append("SPRAS = '{}'".format(l))

    t023t = read_table(
        "T023T",
        fields=["MATKL", "SPRAS", "WGBEZ"],
        where=where,
        connection=connection,
    )

    texts: Dict[str, Dict[str, str]] = {}
    for r in t023t:
        texts.setdefault(r["MATKL"], {})[r["SPRAS"]] = r["WGBEZ"].strip()

    out: Dict[str, Dict[str, object]] = {}
    for r in t023:
        matkl = r["MATKL"]
        out[matkl] = {
            "SPART": r.get("SPART", ""),
            "texts": texts.get(matkl, {}),
        }
    return out


if __name__ == "__main__":  # Manual quick check (requires env vars configured)
    # Example using explicit credentials. Prefer environment variables.
    # Uncomment and adjust if you want to run directly:
    # conn = get_connection(
    #     ashost="sapvirtual1.ddns.net", sysnr="34",
    #     client="500", user="S4USER080", passwd="@Ticart123", lang="EN"
    # )
    # data = fetch_material_groups_with_texts(connection=conn)
    # for i, (matkl, info) in enumerate(data.items()):
    #        print(matkl, info["texts"])
    #        if i >= 9:
    #            break
    pass

