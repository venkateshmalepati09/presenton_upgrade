"""
Complete end-to-end test: Create → Prepare presentation
This demonstrates the correct payload format for both endpoints.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1/ppt"

# Step 1: Create presentation with fetched data
print("=" * 60)
print("STEP 1: Creating presentation with fetch data...")
print("=" * 60)

payload_data = {
    "reportname": "visa dataset report",
    "user_id": "e23221ad-85f0-4fc6-88ec-1aad756a93e3",
    "list_of_queries": [
        "95c31c12-eb34-4693-83d2-26dcd2052add"
    ],
    "Description": "Generate comprehensive data analysis report."
}

create_payload = {
    "content": json.dumps(payload_data),
    "n_slides": 5,
    "language": "English"
}

create_response = requests.post(f"{BASE_URL}/presentation/create", json=create_payload)
print(f"Status: {create_response.status_code}")

if create_response.status_code != 200:
    print(f"Error: {create_response.text}")
    exit(1)

presentation_data = create_response.json()
presentation_id = presentation_data["id"]
print(f"✅ Created presentation: {presentation_id}")
print(f"Content preview: {presentation_data['content'][:200]}...")

# Step 2: Prepare presentation with outlines
print("\n" + "=" * 60)
print("STEP 2: Preparing presentation with outlines...")
print("=" * 60)

# Simple outlines based on the fetched content
outlines = [
    {
        "content": "Introduction to Visa Dataset Analysis\n\nOverview of employment cases by continent and region."
    },
    {
        "content": "Query: how many of continent and region of employment show me in bar chart\n\nResponse: Analysis shows Asia leads with 16,861 cases, followed by Europe (3,732) and North America (3,292)."
    },
    {
        "content": "Regional Distribution\n\nNortheast: 7,195 cases\nSouth: 7,017 cases\nWest: 6,586 cases\nMidwest: 4,307 cases"
    },
    {
        "content": "Key Insights\n\n- Asia dominates with 67% of all cases\n- Northeast region has highest employment concentration\n- Significant geographic diversity in employment patterns"
    },
    {
        "content": "Conclusion\n\nComprehensive analysis reveals clear geographic trends in visa employment data."
    }
]

# Minimal valid layout (you can get real layouts from /api/v1/ppt/template-management/get-templates)
layout = {
    "name": "modern",
    "ordered": False,
    "slides": [
        {
            "id": "title_slide",
            "name": "Title Slide",
            "description": "Title slide layout",
            "json_schema": {
                "type": "object",
                "title": "Title Slide",
                "properties": {
                    "title": {"type": "string"},
                    "subtitle": {"type": "string"}
                },
                "required": ["title"]
            }
        },
        {
            "id": "content_slide",
            "name": "Content Slide",
            "description": "Content slide layout",
            "json_schema": {
                "type": "object",
                "title": "Content Slide",
                "properties": {
                    "heading": {"type": "string"},
                    "content": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["heading"]
            }
        }
    ]
}

prepare_payload = {
    "presentation_id": presentation_id,  # Use the real ID from step 1
    "outlines": outlines,
    "layout": layout,
    "title": "Visa Dataset Analysis Report"
}

prepare_response = requests.post(f"{BASE_URL}/presentation/prepare", json=prepare_payload)
print(f"Status: {prepare_response.status_code}")

if prepare_response.status_code != 200:
    print(f"Error: {prepare_response.text}")
    exit(1)

prepared_data = prepare_response.json()
print(f"✅ Prepared presentation: {prepared_data['id']}")
print(f"Title: {prepared_data['title']}")
print(f"Number of slides: {len(outlines)}")

print("\n" + "=" * 60)
print("✅ SUCCESS! Presentation created and prepared.")
print("=" * 60)
print(f"\nPresentation ID: {presentation_id}")
print(f"Next step: Call GET /api/v1/ppt/presentation/stream/{presentation_id}")
print("to generate the actual slide content.")
