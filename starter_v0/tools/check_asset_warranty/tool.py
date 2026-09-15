from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from tools._shared import ROOT, err

ASSETS_PATH = ROOT / "helpdesk_data" / "assets.json"


def check_asset_warranty(asset_id: str) -> dict[str, Any]:
    """Check warranty status for a given asset ID.

    Args:
        asset_id: The asset ID to look up (e.g., "LT-204").

    Returns:
        A dict with asset_id, warranty_until, is_active, days_remaining,
        and expiration_status ("active", "expiring_soon", or "expired").
    """
    try:
        with open(ASSETS_PATH, encoding="utf-8") as f:
            data = json.load(f)

        asset = None
        for a in data.get("assets", []):
            if a.get("asset_id", "").upper() == asset_id.upper():
                asset = a
                break

        if not asset:
            return {
                "asset_id": asset_id,
                "error": "Asset not found",
                "message": f"No asset found with ID '{asset_id}' in the inventory.",
            }

        warranty_str = asset.get("warranty_until", "")
        if not warranty_str:
            return {
                "asset_id": asset_id,
                "error": "Warranty information missing",
                "message": f"Asset '{asset_id}' has no warranty information recorded.",
            }

        # Parse warranty date
        try:
            warranty_date = datetime.strptime(warranty_str, "%Y-%m-%d").date()
        except ValueError:
            return {
                "asset_id": asset_id,
                "error": "Invalid date format",
                "message": f"Warranty date '{warranty_str}' for asset '{asset_id}' is not in valid format.",
            }

        today = date.today()
        days_remaining = (warranty_date - today).days

        # Determine status
        if days_remaining < 0:
            expiration_status = "expired"
        elif days_remaining <= 30:
            expiration_status = "expiring_soon"
        else:
            expiration_status = "active"

        return {
            "asset_id": asset.get("asset_id"),
            "warranty_until": warranty_str,
            "is_active": days_remaining >= 0,
            "days_remaining": max(days_remaining, 0),
            "expiration_status": expiration_status,
            "asset_type": asset.get("type"),
            "model": asset.get("model"),
            "manufacturer": asset.get("manufacturer"),
        }

    except FileNotFoundError:
        return err("check_asset_warranty", FileNotFoundError(f"Assets database not found at {ASSETS_PATH}"))
    except Exception as e:
        return err("check_asset_warranty", e)
