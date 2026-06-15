# Scaling law in linear regression

Research notes on optimizer-dependent scaling laws for linear regression and random-feature models, with an emphasis on Adam/RMSProp-like adaptive diagonal preconditioning.

Current focus:

1. Fixed spectral preconditioning: replacing SGD by preconditioned SGD with \(P_q = H^{-q}\).
2. Damped spectral preconditioning: \(P_{\rho,q}=(H+\rho I)^{-q}\), the clean proxy for Adam/RMSProp's \(\epsilon\)-damped second-moment preconditioner.
3. Frozen RMSProp: estimating the second-moment preconditioner from gradients and then freezing it.
4. Fully online Adam/RMSProp and AdamW.

Current proof notes:

- [`notes/damped_spectral_preconditioning.md`](notes/damped_spectral_preconditioning.md): oracle damped spectral preconditioning and the two-slope learned-dimension law.
- [`notes/frozen_rmsprop_preconditioning.md`](notes/frozen_rmsprop_preconditioning.md): frozen RMSProp theorem showing that robust second-moment burn-in estimates recover the Adam/RMSProp-like \(q=1/2\) damped preconditioner.
