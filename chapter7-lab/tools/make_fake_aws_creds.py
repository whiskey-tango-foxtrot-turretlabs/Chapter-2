"""Write a FAKE AWS-format credential file for the Lab 1 push-protection test.

The values have the shape of an AWS access key pair, so GitHub secret scanning
recognises them, but they were generated locally and grant nothing.
A fresh random pair is produced on every run.

Usage (from the chapter7-lab folder):
    python tools/make_fake_aws_creds.py
    python tools/make_fake_aws_creds.py --out config/other-file.ini

The file is written as UTF-8 on purpose: in Windows PowerShell 5.1,
`python ... > file` would write UTF-16, which secret scanning cannot match.
"""
import argparse
import pathlib
import secrets
import string

ID_ALPHABET = string.ascii_uppercase + "234567"
SECRET_ALPHABET = string.ascii_letters + string.digits + "+/"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="config/legacy-credentials.ini")
    args = parser.parse_args()

    key_id = "AKIA" + "".join(secrets.choice(ID_ALPHABET) for _ in range(16))
    secret = "".join(secrets.choice(SECRET_ALPHABET) for _ in range(40))

    path = pathlib.Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Copied from a laptop 'just to get the sync script working'\n"
        "[default]\n"
        f"aws_access_key_id = {key_id}\n"
        f"aws_secret_access_key = {secret}\n"
        "region = eu-north-1\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote fake credential pair to {path}")


if __name__ == "__main__":
    main()
