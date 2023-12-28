#!/usr/bin/bash -e


echo "patching 'deployment/console-ui' in a namespace 'default'." >&2
cat <<EOPATCH | kubectl patch --namespace default deployment console-ui --patch-file /Users/anthonyvelasco/work/scripts/right-sizing/console.yaml
EOPATCH
