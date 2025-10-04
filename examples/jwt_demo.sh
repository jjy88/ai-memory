#!/bin/bash
# JWT认证演示脚本
# 展示如何使用新的JWT认证系统

set -e

BASE_URL="${1:-http://localhost:8000}"

echo "========================================="
echo "Obsi喵 AI Memory - JWT认证演示"
echo "Base URL: $BASE_URL"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 用户注册
echo -e "${BLUE}[1/5] 用户注册${NC}"
USERNAME="demo_$(date +%s)"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"demo123\"}")

echo "$REGISTER_RESPONSE" | python -m json.tool
USER_ID=$(echo "$REGISTER_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('user_id', ''))")
echo -e "${GREEN}✓ 注册成功，用户ID: $USER_ID${NC}"
echo ""
sleep 1

# 2. 用户登录
echo -e "${BLUE}[2/5] 用户登录${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"demo123\"}")

echo "$LOGIN_RESPONSE" | python -m json.tool
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")
REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('refresh_token', ''))")
echo -e "${GREEN}✓ 登录成功${NC}"
echo ""
sleep 1

# 3. 验证Access Token
echo -e "${BLUE}[3/5] 验证Access Token${NC}"
VERIFY_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/verify" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "$VERIFY_RESPONSE" | python -m json.tool
echo -e "${GREEN}✓ Access Token验证通过${NC}"
echo ""
sleep 1

# 4. 刷新Token
echo -e "${BLUE}[4/5] 使用Refresh Token获取新的Access Token${NC}"
REFRESH_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/refresh" \
  -H "Authorization: Bearer $REFRESH_TOKEN")

echo "$REFRESH_RESPONSE" | python -m json.tool
NEW_ACCESS_TOKEN=$(echo "$REFRESH_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")
echo -e "${GREEN}✓ 新Access Token获取成功${NC}"
echo ""
sleep 1

# 5. 使用新Token验证
echo -e "${BLUE}[5/5] 验证新的Access Token${NC}"
NEW_VERIFY_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/verify" \
  -H "Authorization: Bearer $NEW_ACCESS_TOKEN")

echo "$NEW_VERIFY_RESPONSE" | python -m json.tool
echo -e "${GREEN}✓ 新Access Token验证通过${NC}"
echo ""

echo "========================================="
echo -e "${GREEN}JWT认证流程演示完成！${NC}"
echo ""
echo "总结:"
echo "  1. 用户注册 -> 获得user_id"
echo "  2. 用户登录 -> 获得access_token和refresh_token"
echo "  3. 使用access_token访问受保护资源"
echo "  4. access_token过期前用refresh_token获取新token"
echo "  5. 继续使用新token访问资源"
echo ""
echo "Token有效期:"
echo "  - Access Token: 7天"
echo "  - Refresh Token: 30天"
echo "========================================="
