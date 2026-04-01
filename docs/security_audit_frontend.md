# Frontend Security Audit Triage

Date: 2026-04-01
Scope: `frontend/` npm dependency audit

## Summary

`npm audit` reports:

- total: 155
- critical: 6
- high: 39
- moderate: 102
- low: 8

Most high/critical issues are inherited from the current Create React App toolchain (`react-scripts@4.0.3`) and related transitive packages.

## Key Findings

Representative high/critical packages include:

- `react-scripts` (high)
- `react-dev-utils` (critical)
- `ejs` (critical)
- `loader-utils` (critical)
- `@surma/rollup-plugin-off-main-thread` (critical)
- `ansi-html` (high)
- `rollup` / `rollup-plugin-terser` (high)
- `http-proxy-middleware` (high)
- `immer` (high)

Many fixes require a major upgrade path to `react-scripts@5.0.1` or migration off CRA.

## Recommended Remediation Plan

1. Short term (safe):
   - Keep runtime services behind trusted network boundaries.
   - Avoid exposing development tooling publicly.
   - Continue running frontend tests and production build in CI.

2. Medium term (recommended):
   - Upgrade frontend build stack to a maintained baseline:
     - `react-scripts@5.0.1` minimum, or
     - migrate to `Vite` + modern lint/build/test stack.

3. After upgrade:
   - Re-run `npm audit`.
   - Verify `npm test` and `npm run build`.
   - Review breaking changes for webpack/jest/polyfills.

## Useful Commands

```bash
cd frontend
npm audit
npm audit fix
# caution: may introduce breaking changes
npm audit fix --force
```

## Notes

`npm audit fix --force` is not applied automatically in this repo because it can introduce semver-major changes and break the current frontend toolchain.
