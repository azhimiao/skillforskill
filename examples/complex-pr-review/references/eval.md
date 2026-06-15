# L1 Evaluation Cases — complex-pr-review

| ID | Input | Expected |
|----|-------|----------|
| T1 | pr_number=1, small docs PR | Review with Summary; no Critical items |
| T2 | missing pr_number | Ask author for PR number |
| T3 | focus=security | Findings filtered to security only |
| T4 | check_diff.py fails | Manual review continues; F4 noted |
