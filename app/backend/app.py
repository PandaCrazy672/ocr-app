from flask import Flask, request, jsonify
from flask_cors import CORS
import os, uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
ALLOWED = set((os.getenv("ALLOWED_EXTS","pdf,jpg,jpeg,png")).split(","))

DB = {"documents":{}, "fields":{}, "audit":[]}

def audit(action, doc_id=None, meta=None):
    DB["audit"].append({
        "ts": datetime.utcnow().isoformat(),
        "action": action, "doc_id": doc_id, "meta": meta or {}
    })

def mock_infer():
    return [
        {"id": str(uuid.uuid4()), "page": 1, "key":"policy_number","value":"AB-123456","conf":0.91,"bbox":[120,220,260,28]},
        {"id": str(uuid.uuid4()), "page": 1, "key":"claimant_name","value":"M. Dupont","conf":0.77,"bbox":[130,270,320,26]},
        {"id": str(uuid.uuid4()), "page": 2, "key":"incident_date","value":"2025-09-18","conf":0.62,"bbox":[140,180,180,24]},
    ]

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "time": datetime.utcnow().isoformat()})

@app.post("/api/documents")
def upload_document():
    f = request.files.get("file")
    if not f:
        return jsonify({"error":"file is required"}), 400
    ext = (f.filename.rsplit(".",1)[-1] or "").lower()
    if ext not in ALLOWED:
        return jsonify({"error":"file type not allowed"}), 415

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    doc_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{doc_id}.{ext}")
    f.save(path)

    DB["documents"][doc_id] = {
        "id": doc_id, "filename": f.filename, "path": path,
        "status":"review", "created_at": datetime.utcnow().isoformat(), "pages":[1,2]
    }
    DB["fields"][doc_id] = mock_infer()
    audit("upload", doc_id, {"filename": f.filename})
    audit("inference_complete", doc_id, {"num_fields": len(DB["fields"][doc_id])})

    return jsonify({"id": doc_id, "status":"review"}), 201

@app.get("/api/documents/<doc_id>/fields")
def get_fields(doc_id):
    if doc_id not in DB["documents"]:
        return jsonify({"error":"not found"}), 404
    return jsonify(DB["fields"].get(doc_id, []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
