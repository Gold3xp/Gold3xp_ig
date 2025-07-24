#!/data/data/com.termux/files/usr/bin/bash

GREEN="\033[1;32m"
CYAN="\033[1;36m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
NC="\033[0m"

echo -e "${CYAN}🚀 Memulai setup otomatis Gold3xp_ig di Termux...${NC}"
pkg update -y && pkg upgrade -y
pkg install -y git python clang libffi libcrypt openssl zlib libjpeg-turbo \
    make build-essential openssl-tool libxml2 libxslt libzmq libjpeg-turbo pyenv

if [ ! -d "$HOME/.pyenv" ]; then
  echo -e "${YELLOW}🔧 Menginstal pyenv...${NC}"
  curl https://pyenv.run | bash
fi

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

if ! pyenv versions | grep -q "3.9.18"; then
  echo -e "${YELLOW}🐍 Menginstall Python 3.9.18...${NC}"
  CFLAGS="-I/data/data/com.termux/files/usr/include" \
  LDFLAGS="-L/data/data/com.termux/files/usr/lib" \
  pyenv install 3.9.18
fi

if [ ! -d "$HOME/.pyenv/versions/igvenv" ]; then
  echo -e "${YELLOW}🧪 Membuat virtualenv 'igvenv'...${NC}"
  pyenv virtualenv 3.9.18 igvenv
fi

pyenv activate igvenv

echo -e "${YELLOW}📦 Menginstall requirements.txt...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}✅ Selesai! Jalankan: python gacor.py${NC}"
