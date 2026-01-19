#!/bin/bash

REVIEW_ID="886a0576-488e-48a8-9e1c-f8ff2b5069ee"
USER_ID="48de0169-fbeb-4f75-a3b5-08491a966269"
PLACE_ID="1ea9b0cd-a368-4bfc-ab01-1f13be3dad89"

echo "=== Update Review ==="
curl -s -X PUT "http://localhost:5000/api/v1/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Updated!\", \"rating\": 4, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}"
echo ""
echo ""

echo "=== Get Updated Review ==="
curl -s -X GET "http://localhost:5000/api/v1/reviews/$REVIEW_ID"
echo ""
echo ""

echo "=== Delete Review ==="
curl -s -X DELETE "http://localhost:5000/api/v1/reviews/$REVIEW_ID"
echo ""
echo ""

echo "=== Verify Deletion (should be 404) ==="
curl -s -X GET "http://localhost:5000/api/v1/reviews/$REVIEW_ID"
echo ""
