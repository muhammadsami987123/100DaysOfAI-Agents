import os
import tempfile
from typing import Optional

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

try:
    from . import config  # type: ignore
    from .crypto_core import encrypt_file, decrypt_file  # type: ignore
    from .logger import log_event  # type: ignore
except Exception:  # Support running as script: python web_server.py
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import config  # type: ignore
    from crypto_core import encrypt_file, decrypt_file  # type: ignore
    from logger import log_event  # type: ignore


def create_app() -> Flask:
    config.ensure_directories()
    app = Flask(__name__)
    app.secret_key = os.environ.get("FILE_ENC_SECRET", os.urandom(16))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/encrypt", methods=["POST"])
    def route_encrypt():
        up = request.files.get("file")
        pw = request.form.get("password", "")
        pw2 = request.form.get("password_confirm", "")
        if not up or up.filename == "":
            flash("Please choose a file.", "error")
            return redirect(url_for("index"))
        if not pw:
            flash("Password required.", "error")
            return redirect(url_for("index"))
        if pw != pw2:
            flash("Passwords do not match.", "error")
            return redirect(url_for("index"))
        # Save upload to temp, then encrypt
        with tempfile.TemporaryDirectory() as td:
            temp_in = os.path.join(td, up.filename)
            up.save(temp_in)
            out_name = up.filename + ".enc"
            out_path = os.path.join(config.ENCRYPTED_DIR, out_name)
            try:
                encrypt_file(temp_in, out_path, pw)
                log_event("encrypt_success_web", {"input": up.filename, "output": out_name})
                flash(f"Encrypted to {out_name}", "success")
                return redirect(url_for("download_encrypted", filename=out_name))
            except Exception as exc:
                log_event("encrypt_error_web", {"input": up.filename, "error": str(exc)})
                flash(f"Encrypt failed: {exc}", "error")
                return redirect(url_for("index"))

    @app.route("/decrypt", methods=["POST"])
    def route_decrypt():
        up = request.files.get("file")
        pw = request.form.get("password", "")
        if not up or up.filename == "":
            flash("Please choose a .enc file.", "error")
            return redirect(url_for("index"))
        if not pw:
            flash("Password required.", "error")
            return redirect(url_for("index"))
        base = up.filename
        if base.lower().endswith(".enc"):
            base = base[: -len(".enc")]
        with tempfile.TemporaryDirectory() as td:
            temp_in = os.path.join(td, up.filename)
            up.save(temp_in)
            out_name = base
            out_path = os.path.join(config.DECRYPTED_DIR, out_name)
            try:
                decrypt_file(temp_in, out_path, pw)
                log_event("decrypt_success_web", {"input": up.filename, "output": out_name})
                flash(f"Decrypted to {out_name}", "success")
                return redirect(url_for("download_decrypted", filename=out_name))
            except Exception as exc:
                log_event("decrypt_error_web", {"input": up.filename, "error": str(exc)})
                flash(f"Decrypt failed: {exc}", "error")
                return redirect(url_for("index"))

    @app.route("/download/encrypted/<path:filename>")
    def download_encrypted(filename: str):
        return send_from_directory(config.ENCRYPTED_DIR, filename, as_attachment=True)

    @app.route("/download/decrypted/<path:filename>")
    def download_decrypted(filename: str):
        return send_from_directory(config.DECRYPTED_DIR, filename, as_attachment=True)

    return app


def main() -> None:
    app = create_app()
    app.run(host="127.0.0.1", port=5005, debug=False)


if __name__ == "__main__":
    main()


