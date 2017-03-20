#!/bin/bash
# need  pywin32

PRONAME=Enchain
PRODIR=/home/zhehua/Github/Enchain

cur_path=`pwd`
cd ${PRODIR}
rm -rf ${PRODIR}/build/
mkdir -p ${PRODIR}/dist
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
cp -f ${PRODIR}/dist/${PRONAME} ~/
rm -f ${PRODIR}/dist/${PRONAME}
cd ${cur_path}