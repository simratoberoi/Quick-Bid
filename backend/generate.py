def generate_proposal(rfp_row):
    """Generate a professional proposal based on matched RFP and product"""
    
    # Extract technical specs if available
    tech_specs = rfp_row.get('tech_specs', {})
    
    proposal = f"""
================================================================================
PROPOSAL FOR REQUEST FOR PROPOSAL
================================================================================

RFP ID: {rfp_row['rfp_id']}
Title: {rfp_row['title']}
Organization: {rfp_row.get('organization', 'N/A')}
Deadline: {rfp_row.get('deadline', 'N/A')}

--------------------------------------------------------------------------------
MATCH ANALYSIS
--------------------------------------------------------------------------------
Match Confidence: {rfp_row['match_percent']}%
Matched SKU: {rfp_row['matched_sku']}

--------------------------------------------------------------------------------
PROPOSED SOLUTION
--------------------------------------------------------------------------------

Product Name: {rfp_row['matched_product_name']}
Category: {rfp_row['matched_category']}
SKU: {rfp_row['matched_sku']}

Technical Specifications:
• Conductor Material: {rfp_row.get('matched_conductor_material', 'N/A')}
• Conductor Size: {rfp_row.get('matched_conductor_size', 'N/A')} sqmm
• Voltage Rating: {rfp_row.get('matched_voltage_rating', 'N/A')} kV
• Compliance Standard: {rfp_row['matched_standard']}

--------------------------------------------------------------------------------
PRICING
--------------------------------------------------------------------------------
Unit Price: ₹{rfp_row['unit_price']:,.2f} INR
Testing Price: ₹{rfp_row['test_price']:,.2f} INR
Total Base Price: ₹{(rfp_row['unit_price'] + rfp_row['test_price']):,.2f} INR

(Final pricing will be provided based on quantity requirements)

--------------------------------------------------------------------------------
WHY CHOOSE US
--------------------------------------------------------------------------------
✓ Full compliance with international standards ({rfp_row['matched_standard']})
✓ High-quality {rfp_row.get('matched_conductor_material', '')} conductor materials
✓ Rigorous type testing and routine testing procedures
✓ Competitive pricing with transparent cost structure
✓ Fast delivery and dedicated project support
✓ ISO certified manufacturing facilities
✓ Comprehensive warranty and after-sales service

--------------------------------------------------------------------------------
DELIVERY & TERMS
--------------------------------------------------------------------------------
• Expected Delivery: As per RFP requirements
• Payment Terms: Negotiable
• Validity: 90 days from proposal date
• Warranty: As per standard terms

--------------------------------------------------------------------------------
COMPLIANCE STATEMENT
--------------------------------------------------------------------------------
We confirm that our proposed product meets all technical specifications
mentioned in the RFP document, including:
- Conductor specifications and resistance requirements
- Insulation thickness and material standards
- Voltage ratings and test voltage requirements
- Compliance with {rfp_row['matched_standard']} standards
- Successful completion of type and routine tests

We look forward to the opportunity to support your project and deliver
high-quality solutions that meet your requirements.

Best Regards,
[Your Company Name]
[Contact Information]

================================================================================
"""
    return proposal
