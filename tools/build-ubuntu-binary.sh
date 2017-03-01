#!/bin/bash

PRODIR=`pwd`
PRONAME=Enchain

rm -rf ${PRODIR}/build/
rm -rf ${PRODIR}/dist/
rm -rf ${PRODIR}/build/${PRONAME}.spec

${PRODIR}/pyinstaller/pyinstaller.py \
                    --hidden-import=numpy \
                    --hidden-import=sys \
                    --hidden-import=os \
                    --hidden-import=shutil \
                    -F  \
                    --specpath ${PRODIR}/build/ \
                    -p ${PRODIR}/ui \
                    -p ${PRODIR}/libs \
                    -n ${PRONAME} \
                     ${PRODIR}/Enchain.py


rm -rf ${PRODIR}/build/
mv ${PRODIR}/dist/${PRONAME} ~/${PRONAME}