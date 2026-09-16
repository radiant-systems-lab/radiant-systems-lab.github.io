#!/usr/bin/env bash
# Deploy the class-lab backend and point the lab pages at it.
#
#   infra/labs-backend/deploy.sh test     # the stack used while trying things out
#   infra/labs-backend/deploy.sh prod     # the real one; keeps data if the stack is deleted
#
# Needs the AWS CLI and a signed-in profile:   aws sso login --profile bhanu
# Override defaults with environment variables, for example:
#   OWNERS="a@missouri.edu,b@umsystem.edu" AWS_PROFILE=other ./deploy.sh test
set -euo pipefail

STAGE="${1:?usage: deploy.sh test|prod}"
case "$STAGE" in test|prod) ;; *) echo "stage must be test or prod" >&2; exit 2 ;; esac

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PROFILE="${AWS_PROFILE:-bhanu}"
REGION="${AWS_REGION:-us-east-1}"
STACK="csc-ee-8001-labs-$STAGE"
OWNERS="${OWNERS:-bv3hz@umsystem.edu,bv3hz@missouri.edu,tanu@missouri.edu}"
if [ "$STAGE" = prod ]; then
  ORIGINS="${ORIGINS:-https://radiant-systems-lab.github.io}"
else
  ORIGINS="${ORIGINS:-https://radiant-systems-lab.github.io,http://127.0.0.1:8931,http://localhost:4000}"
fi

aws_() { aws --profile "$PROFILE" --region "$REGION" "$@"; }
# On Windows the AWS CLI cannot read Git Bash paths inside file:// links.
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else echo "$1"; fi; }

ACCOUNT="$(aws_ sts get-caller-identity --query Account --output text)"
BUCKET="csc-ee-8001-labs-artifacts-$ACCOUNT-$REGION"
echo "account $ACCOUNT, stack $STACK, owners $OWNERS"

# Lambda code is uploaded here before CloudFormation can use it.
if ! aws_ s3api head-bucket --bucket "$BUCKET" >/dev/null 2>&1; then
  echo "creating artifact bucket $BUCKET"
  if [ "$REGION" = us-east-1 ]; then
    aws_ s3api create-bucket --bucket "$BUCKET" >/dev/null
  else
    aws_ s3api create-bucket --bucket "$BUCKET" \
      --create-bucket-configuration LocationConstraint="$REGION" >/dev/null
  fi
  aws_ s3api put-public-access-block --bucket "$BUCKET" --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
  aws_ s3api put-bucket-lifecycle-configuration --bucket "$BUCKET" --lifecycle-configuration \
    '{"Rules":[{"ID":"expire-old-builds","Status":"Enabled","Filter":{},"Expiration":{"Days":30}}]}'
  aws_ s3api put-bucket-tagging --bucket "$BUCKET" \
    --tagging 'TagSet=[{Key=project,Value=csc-ee-8001-labs}]'
fi

BUILD="$HERE/.build"
mkdir -p "$BUILD"
# The unit tests leave bytecode next to the sources; keep it out of the upload.
find "$HERE/src" -name __pycache__ -type d -prune -exec rm -rf {} +
aws_ cloudformation package \
  --template-file "$HERE/template.yaml" \
  --s3-bucket "$BUCKET" --s3-prefix "$STACK" \
  --output-template-file "$BUILD/packaged-$STAGE.yaml" >/dev/null

# CommaDelimitedList values contain commas, so they are passed through a file.
python - "$BUILD/params-$STAGE.json" "$STAGE" "$OWNERS" "$ORIGINS" <<'PY'
import json, sys
path, stage, owners, origins = sys.argv[1:]
json.dump([
    {"ParameterKey": "Stage", "ParameterValue": stage},
    {"ParameterKey": "OwnerEmails", "ParameterValue": owners},
    {"ParameterKey": "AllowedOrigins", "ParameterValue": origins},
], open(path, "w"))
PY

aws_ cloudformation deploy \
  --stack-name "$STACK" \
  --template-file "$BUILD/packaged-$STAGE.yaml" \
  --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
  --parameter-overrides "file://$(native "$BUILD/params-$STAGE.json")" \
  --tags project=csc-ee-8001-labs stage="$STAGE" \
  --no-fail-on-empty-changeset

output() {
  aws_ cloudformation describe-stacks --stack-name "$STACK" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text
}
API_URL="$(output ApiUrl)"
POOL_ID="$(output UserPoolId)"
CLIENT_ID="$(output UserPoolClientId)"
ALIASES="$(output AliasDomains)"

# These three values are public by design: every browser that loads a lab needs them.
CONFIG="$REPO/labs/gate/config.js"
cat > "$CONFIG" <<JS
// Written by infra/labs-backend/deploy.sh for the "$STAGE" stack. Safe to publish.
window.RADIANT_LAB_CONFIG = {
  stage: "$STAGE",
  region: "$REGION",
  apiUrl: "$API_URL",
  userPoolId: "$POOL_ID",
  clientId: "$CLIENT_ID",
  // These domains are one mailbox; sign-in folds them into the first one.
  aliasDomains: "$ALIASES".split(","),
};
JS
echo
echo "API          $API_URL"
echo "User pool    $POOL_ID"
echo "App client   $CLIENT_ID"
echo "Wrote        labs/gate/config.js"
