from flask import Flask, request, abort
from pathlib import Path
import logging

import logic.split as sp
import logic.merge as mg
import logic.extract_pages as ex
import logic.save_securely as sec
import logic.constants as co

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")


@app.errorhandler(400)
def required_data_not_provided(_):
    return "Required key(s) not passed!", 400


@app.errorhandler(404)
def source_does_not_exist(_):
    return "Source path does not exist!", 404


@app.route('/split', methods=["POST"])
def split():
    """Split a pdf into separate pages. Requires path to the file."""
    kwargs = {}
    try:
        source_path = Path(request.form[co.source_path])
        kwargs[co.source_path] = source_path
    except KeyError as er:
        app.logger.error(co.incorrect_body_message.format(er.args[0]))
        abort(400)
    if co.destination in request.form:
        kwargs[co.destination] = Path(request.form[co.destination])
    try:
        save_path = sp.split_and_save_pdf(**kwargs)
        return f"Split {source_path.name} and saved in {save_path}."
    except FileNotFoundError as er:
        app.logger.error(er)
        abort(404)


@app.route('/merge', methods=['POST'])
def merge():
    """Merge several pdf pages from folder into a single pdf.
     Requires path to the folder and optional merged pdf name and overwrite flag."""
    kwargs = {}
    try:
        source_path = Path(request.form[co.source_path])
        kwargs[co.source_path] = source_path
    except KeyError as er:
        app.logger.error(co.incorrect_body_message.format(er.args[0]))
        abort(400)
    if co.merged_pdf_name in request.form:
        kwargs[co.merged_pdf_name] = request.form[co.merged_pdf_name]
    if co.overwrite in request.form:
        kwargs[co.overwrite] = bool(request.form[co.overwrite])
    if co.destination in request.form:
        kwargs[co.destination] = Path(request.form[co.destination])

    try:
        save_path = mg.merge_and_save_pdf(**kwargs)
        return f"Merged files from {source_path.name} and saved into {save_path}."
    except co.FolderNotFound as er:
        app.logger.error(er)
        abort(404)


@app.route('/extract', methods=['POST'])
def extract():
    """Extract pages selectively and save them as one pdf.
    Requires path to the pdf and pages' numbers to extract. Optional overwrite flag."""
    kwargs = {}
    try:
        source_path = Path(request.form[co.source_path])
        pages = request.form[co.pages]
        kwargs[co.source_path] = source_path
        kwargs[co.pages] = pages
    except KeyError as er:
        app.logger.error(co.incorrect_body_message.format(er.args[0]))
        abort(400)
    if co.overwrite in request.form:
        kwargs[co.overwrite] = bool(request.form[co.overwrite])
    if co.destination in request.form:
        kwargs[co.destination] = Path(request.form[co.destination])
    try:
        save_path = ex.extract_and_save_pages(**kwargs)
        return f"Extracted pages {pages} and saved into {save_path}."
    except FileNotFoundError as er:
        app.logger.error(er)
        abort(404)


@app.route('/save-securely', methods=['POST'])
def save_securely():
    """Protect pdf with password.
    Requires path to the pdf. Both user and owner passwords are optional, however specifying only one or none
    makes no protection. Also optional overwrite flag."""
    kwargs = {}
    try:
        source_path = Path(request.form[co.source_path])
        kwargs[co.source_path] = source_path
    except KeyError as er:
        app.logger.error(co.incorrect_body_message.format(er.args[0]))
        abort(400)
    if co.owner_pass in request.form:
        kwargs[co.owner_pass] = request.form[co.owner_pass]
    if co.user_pass in request.form:
        kwargs[co.user_pass] = request.form[co.user_pass]
    if co.overwrite in request.form:
        kwargs[co.overwrite] = bool(request.form[co.overwrite])
    if co.destination in request.form:
        kwargs[co.destination] = Path(request.form[co.destination])
    try:
        save_path = sec.save_pdf_securely(**kwargs)
        return f"Password-protected and saved into {save_path}."
    except FileNotFoundError as er:
        app.logger.error(er)
        abort(404)


if __name__ == "__main__":
    app.run()
