# Signed rule channel — intentionally empty

The observation catalog under `docs/data/` is not app-consumable. A future rule package requires exact package, signer, bounded versions, deterministic canonical payload, offline ECDSA P-256/SHA-256 signature, monotonic version, expiry, review and an immutable GitHub Release.

The private key stays offline and outside GitHub. Adding JSON here currently fails CI by design; the gate must be upgraded together with a real signature verifier before the first rule release.
