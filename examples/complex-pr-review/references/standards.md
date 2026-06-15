# PR Review Standards

## Critical (must fix before merge)

- Security: secrets, credentials, or tokens in code or config
- Security: SQL injection, XSS, or unsafe deserialization
- Correctness: logic errors that break existing behavior without tests
- Correctness: missing error handling on external I/O

## Suggestion (should fix)

- Maintainability: functions over 50 lines without clear structure
- Tests: behavior change without corresponding test update
- API: breaking public interface change without migration note

## Nice-to-have

- Style: naming inconsistent with surrounding module
- Docs: public API missing docstring when peers have one

## Focus filters

| focus | Include sections |
|-------|------------------|
| security | Critical security rows only |
| performance | Critical correctness + performance patterns |
| style | Suggestion style + Nice-to-have |
| full | All sections |
