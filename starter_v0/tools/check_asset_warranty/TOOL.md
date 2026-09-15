---
name: check_asset_warranty
track: bonus
kind: local_inventory
provider: mock_device_inventory
requires_env: []
inputs: [asset_id]
outputs: [asset_id, warranty_until, is_active, days_remaining, expiration_status]
side_effect: false
---
# check_asset_warranty

Looks up the warranty status for one company asset by its asset ID.
Returns the warranty expiration date, active status, days remaining,
and a human-readable expiration status (active, expiring_soon, or expired).
This tool does not modify any data and requires no confirmation.
