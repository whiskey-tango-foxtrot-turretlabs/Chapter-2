# stockroom-api (Chapter 7 lab)

> **Deliberately vulnerable training code.** `app.py` contains SQL injection,
> path traversal and command injection on purpose (marked `LAB-VULN-1..3`) so
> CodeQL has something to find. Do not deploy it or copy those patterns.

Small Flask service used for the Chapter 7 Security & Supply Chain labs.

Run the tests locally:

    python -m pip install -r requirements.txt
    python -m pytest -q

Lab helpers:

- `tools/make_fake_aws_creds.py` - writes a fake AWS-format key pair for the
  push-protection test (Lab 1). Never commit real credentials.
