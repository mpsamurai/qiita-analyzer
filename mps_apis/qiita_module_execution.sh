#!/bin/bash
# djangoへのパスを通す
export QIITA_TOOL=/Users/hiroshiteraoka/MPS/mps_website/qiita-analyzer/mps_apis
export PYTHONPATH=$QIITA_TOOL:$PYTHONPATH


# パスを通す
cmd="mps_apis/"
eval ${cmd}

script="python article_collection.py"
eval ${script}
