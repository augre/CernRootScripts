find . -type d -exec sh -c '(cd {} && tkmain.py -f voigt -o voigt.png > voigt.txt)' ';'
find . -type d -exec sh -c '(cd {} && tkmain.py -f tripleGaussian -o gaus.png > gaus.txt)' ';'
find . -maxdepth 2 -type f \( -name "voigt.*" -or -name "gaus.*" \) -print | zip "${PWD##*/}" -@
