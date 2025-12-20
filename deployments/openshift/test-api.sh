#!/bin/bash
# SAMMO Fight IQ - API Test Script
# Tests all API endpoints after deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get API URL from OpenShift route
PROJECT_NAME="${OPENSHIFT_PROJECT:-sammo-fight-iq}"

echo -e "${GREEN}🥊 SAMMO Fight IQ - API Test Suite${NC}"
echo "========================================"
echo ""

# Get route
API_URL=$(oc get route sammo-fight-iq -n $PROJECT_NAME -o jsonpath='{.spec.host}' 2>/dev/null)

if [ -z "$API_URL" ]; then
    echo -e "${RED}❌ Could not find route. Is the app deployed?${NC}"
    exit 1
fi

API_URL="https://$API_URL"
echo -e "${BLUE}API URL: $API_URL${NC}"
echo ""

# Test 1: Root endpoint
echo -e "${YELLOW}Test 1: Root Endpoint (/)${NC}"
echo "GET $API_URL/"
RESPONSE=$(curl -s "$API_URL/")
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
echo ""

# Test 2: Health check
echo -e "${YELLOW}Test 2: Health Check (/health)${NC}"
echo "GET $API_URL/health"
RESPONSE=$(curl -s "$API_URL/health")
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

# Check if healthy
if echo "$RESPONSE" | grep -q '"status": "healthy"'; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
fi
echo ""

# Test 3: Log a round
echo -e "${YELLOW}Test 3: Log Round (POST /api/log_round)${NC}"
echo "POST $API_URL/api/log_round"
ROUND_DATA='{
  "pressure_score": 8.0,
  "ring_control_score": 7.5,
  "defense_score": 6.0,
  "clean_shots_taken": 2,
  "notes": "Test round from API test script"
}'
echo "Payload: $ROUND_DATA"
RESPONSE=$(curl -s -X POST "$API_URL/api/log_round" \
  -H "Content-Type: application/json" \
  -d "$ROUND_DATA")
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

# Extract round ID
ROUND_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)
if [ "$ROUND_ID" != "null" ] && [ -n "$ROUND_ID" ]; then
    echo -e "${GREEN}✅ Round logged successfully (ID: $ROUND_ID)${NC}"
else
    echo -e "${RED}❌ Failed to log round${NC}"
fi
echo ""

# Test 4: Dashboard stats
echo -e "${YELLOW}Test 4: Dashboard Stats (GET /api/dashboard_stats)${NC}"
echo "GET $API_URL/api/dashboard_stats"
RESPONSE=$(curl -s "$API_URL/api/dashboard_stats")
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

TOTAL_ROUNDS=$(echo "$RESPONSE" | jq -r '.total_rounds' 2>/dev/null)
if [ "$TOTAL_ROUNDS" != "null" ] && [ -n "$TOTAL_ROUNDS" ]; then
    echo -e "${GREEN}✅ Dashboard stats retrieved (Total rounds: $TOTAL_ROUNDS)${NC}"
else
    echo -e "${RED}❌ Failed to get dashboard stats${NC}"
fi
echo ""

# Test 5: Rounds history
echo -e "${YELLOW}Test 5: Rounds History (GET /api/rounds_history)${NC}"
echo "GET $API_URL/api/rounds_history?limit=5"
RESPONSE=$(curl -s "$API_URL/api/rounds_history?limit=5")
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

ROUNDS_COUNT=$(echo "$RESPONSE" | jq -r '.total' 2>/dev/null)
if [ "$ROUNDS_COUNT" != "null" ] && [ -n "$ROUNDS_COUNT" ]; then
    echo -e "${GREEN}✅ Rounds history retrieved ($ROUNDS_COUNT rounds)${NC}"
else
    echo -e "${RED}❌ Failed to get rounds history${NC}"
fi
echo ""

# Test 6: Log another round with different scores
echo -e "${YELLOW}Test 6: Log High Danger Round${NC}"
ROUND_DATA='{
  "pressure_score": 5.0,
  "ring_control_score": 4.0,
  "defense_score": 3.0,
  "clean_shots_taken": 7,
  "notes": "High danger test scenario"
}'
echo "POST $API_URL/api/log_round"
RESPONSE=$(curl -s -X POST "$API_URL/api/log_round" \
  -H "Content-Type: application/json" \
  -d "$ROUND_DATA")
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

DANGER_SCORE=$(echo "$RESPONSE" | jq -r '.danger_score' 2>/dev/null)
STRATEGY=$(echo "$RESPONSE" | jq -r '.strategy.title' 2>/dev/null)
if [ "$DANGER_SCORE" != "null" ] && [ -n "$DANGER_SCORE" ]; then
    echo -e "${GREEN}✅ High danger round logged${NC}"
    echo "   Danger Score: $DANGER_SCORE"
    echo "   Strategy: $STRATEGY"
else
    echo -e "${RED}❌ Failed to log high danger round${NC}"
fi
echo ""

# Test 7: Error handling - invalid data
echo -e "${YELLOW}Test 7: Error Handling (Invalid Data)${NC}"
INVALID_DATA='{"pressure_score": "invalid"}'
echo "POST $API_URL/api/log_round (with invalid data)"
RESPONSE=$(curl -s -X POST "$API_URL/api/log_round" \
  -H "Content-Type: application/json" \
  -d "$INVALID_DATA")
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

if echo "$RESPONSE" | grep -q '"status": "error"'; then
    echo -e "${GREEN}✅ Error handling works correctly${NC}"
else
    echo -e "${YELLOW}⚠️  Unexpected response for invalid data${NC}"
fi
echo ""

# Summary
echo "========================================"
echo -e "${GREEN}✅ API Test Suite Complete${NC}"
echo ""
echo "Summary:"
echo "  API URL: $API_URL"
echo "  All endpoints tested"
echo "  Total rounds logged: 2"
echo ""
echo "To view logs:"
echo "  oc logs -f deployment/sammo-fight-iq -n $PROJECT_NAME"
echo ""
