from flask import Flask, jsonify, request
from scrape import scrape_rfps
from match import match_rfps_with_catalogue
from generate import generate_proposal
import pandas as pd

app = Flask(__name__)

# --------------------------------------------------------
# Health Check
# --------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "✓ Backend running",
        "message": "RFP Automation API",
        "endpoints": {
            "/": "Health check",
            "/run": "Run full pipeline (scrape → match → generate)",
            "/scrape": "Scrape RFPs only",
            "/match": "Match scraped RFPs with catalogue",
            "/proposals": "Generate proposals from matched data"
        }
    })


# --------------------------------------------------------
# Main Pipeline: Scrape → Match → Generate
# --------------------------------------------------------
@app.route("/run", methods=["GET"])
def run_pipeline():
    """Complete pipeline: scrape RFPs, match with catalogue, generate proposals"""
    try:
        print("\n" + "="*60)
        print("STARTING RFP AUTOMATION PIPELINE")
        print("="*60)
        
        # 1. SCRAPE RFP LISTINGS
        print("\n[1/3] Scraping RFP listings...")
        scraped_df = scrape_rfps()
        
        if scraped_df is None or scraped_df.empty:
            return jsonify({
                "error": "Scraping returned no results",
                "step": "scraping"
            }), 500

        # 2. MATCH AGAINST CATALOGUE
        print("\n[2/3] Matching RFPs with product catalogue...")
        matched_df = match_rfps_with_catalogue(scraped_df)
        
        if matched_df is None or matched_df.empty:
            return jsonify({
                "error": "Matching failed",
                "step": "matching"
            }), 500

        # 3. GENERATE PROPOSALS
        print("\n[3/3] Generating proposals...")
        proposals = []
        for idx, row in matched_df.iterrows():
            proposal_text = generate_proposal(row)
            
            proposals.append({
                "rfp_id": row.get("rfp_id"),
                "title": row.get("title"),
                "organization": row.get("organization"),
                "deadline": row.get("deadline"),
                "matched_sku": row.get("matched_sku"),
                "match_percent": float(row.get("match_percent", 0)),
                "matched_product": row.get("matched_product_name"),
                "unit_price": float(row.get("unit_price", 0)),
                "proposal": proposal_text
            })
        
        print(f"\n✓ Pipeline completed successfully!")
        print(f"  - Scraped: {len(scraped_df)} RFPs")
        print(f"  - Matched: {len(matched_df)} RFPs")
        print(f"  - Generated: {len(proposals)} proposals")
        print("="*60 + "\n")

        # Return results
        return jsonify({
            "success": True,
            "summary": {
                "total_rfps": len(scraped_df),
                "matched_rfps": len(matched_df),
                "proposals_generated": len(proposals),
                "avg_match_score": float(matched_df["match_percent"].mean())
            },
            "scraped_rfps": scraped_df.to_dict(orient="records"),
            "match_results": matched_df[["rfp_id", "title", "matched_sku", "match_percent"]].to_dict(orient="records"),
            "proposals": proposals
        })

    except Exception as e:
        print(f"\n✗ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


# --------------------------------------------------------
# Individual Pipeline Steps (for debugging)
# --------------------------------------------------------
@app.route("/scrape", methods=["GET"])
def scrape_only():
    """Scrape RFPs only"""
    try:
        df = scrape_rfps()
        if df is None or df.empty:
            return jsonify({"error": "No RFPs found"}), 404
        
        return jsonify({
            "success": True,
            "count": len(df),
            "data": df.to_dict(orient="records")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/match", methods=["POST"])
def match_only():
    """Match existing scraped data with catalogue"""
    try:
        # Load scraped data
        df = pd.read_csv("scraped_rfps.csv")
        matched_df = match_rfps_with_catalogue(df)
        
        if matched_df is None:
            return jsonify({"error": "Matching failed"}), 500
        
        return jsonify({
            "success": True,
            "count": len(matched_df),
            "data": matched_df.to_dict(orient="records")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------
# Local Server
# --------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "="*60)
    print("RFP AUTOMATION BACKEND SERVER")
    print("="*60)
    print("\nEndpoints:")
    print("  GET  /          - Health check")
    print("  GET  /run       - Run complete pipeline")
    print("  GET  /scrape    - Scrape RFPs only")
    print("  POST /match     - Match scraped RFPs")
    print("\nStarting server on http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)