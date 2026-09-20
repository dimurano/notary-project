@app.get("/api/v1/notary/signing-url/{agreement_id}")
def get_signing_url(agreement_id: str):
    """Fetches the embeddable signing URL for a specific document."""
    url = f"{ADOBE_API_BASE_URL}/agreements/{agreement_id}/signingUrls"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch signing URL")
        
    # Extract the signing URL for the first participant
    signing_urls_info = response.json().get("signingUrlSetInfos", [])
    if signing_urls_info:
        return {"signing_url": signing_urls_info[0]["signingUrls"][0]["es_url"]}
        
    raise HTTPException(status_code=404, detail="No signing URL available")
