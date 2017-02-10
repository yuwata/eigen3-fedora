#!/bin/bash

set -o pipefail

BRANCH=3.3

CMD=${0##*/}
SOURCE_DIR=$(cd $(dirname $0) && pwd)
REPO_NAME=${SOURCE_DIR##*/}
REPO_DIR=${HOME}/git/${REPO_NAME}

HASH_OLD=$(grep -e '^[%#]global commit' ${SOURCE_DIR}/${REPO_NAME}.spec | awk '{ print $3 }')
if [[ -z $HASH_OLD ]]; then
    echo 'error: cannot obtain commit hash.' >&2
    exit 1
fi
HASH_OLD_SHORT=${HASH_OLD:0:7}

if ! hg -R $REPO_DIR pull; then
    echo "error: 'hg pull' failed." >&2
    exit 11
fi

if ! HASH_NEW=$(hg -R $REPO_DIR branches | grep -e "^${BRANCH}" | awk -F : '{ print $2 }'); then
    echo "error: 'hg branches' failed." >&2
    exit 12
fi
HASH_NEW_SHORT=${HASH_NEW:0:7}

if [[ "$HASH_NEW" != "$HASH_OLD" ]]; then

    VERSION=$(grep -e '^Version:' ${SOURCE_DIR}/${REPO_NAME}.spec | awk '{ print $2 }')

    RELEASE_OLD=$(grep -e '^Release:' ${SOURCE_DIR}/${REPO_NAME}.spec | sed -e 's/^Release:[[:space:]]*//; s/%.*$//;')
    RELEASE_MAIN=$(echo $RELEASE_OLD | sed -e 's/\.[[:digit:]]*//')
    RELEASE_SUB_OLD=$(echo $RELEASE_OLD | sed -e 's/[[:digit:]]*\.*//')
    if [[ -z $RELEASE_SUB_OLD ]]; then
        RELEASE_SUB_OLD=0
    fi

    RELEASE_SUB_NEW=$(( $RELEASE_SUB_OLD + 1 ))
    RELEASE_NEW=${RELEASE_MAIN}.${RELEASE_SUB_NEW}

    WEEKDAY=$(date "+%a")
    MONTH=$(date "+%b")
    DAY=$(date "+%d")
    YEAR=$(date "+%Y")

    sed -e '/^[%#]global commit/ { s/^#/%/; s/'${HASH_OLD}'/'${HASH_NEW}'/ }' \
        -e '/^Release:/ s/'${RELEASE_OLD}'/'${RELEASE_NEW}'/' \
        -e "/^%changelog/ a\
* ${WEEKDAY} ${MONTH} ${DAY} ${YEAR} Yu Watanabe <watanabe.yu@gmail.com> - ${VERSION}-${RELEASE_NEW}.hg${HASH_NEW_SHORT}\\
- Update to latest snapshot ${HASH_NEW}\\
" \
        -i ${SOURCE_DIR}/${REPO_NAME}.spec

    git -C $SOURCE_DIR commit -a -m 'Update to latest snapshot'
fi
