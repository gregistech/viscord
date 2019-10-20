# Maintainer: Leo_L <Leo dot Lahtinen at protonmail dot com>
pkgname=viscord-python-git
_pkgname=viscord
pkgver=r62.1bef73e
pkgrel=1
pkgdesc="ncurses based Discord client with vim-like keybindings written in Python"
arch=(i686 x86_64)
url="https://github.com/thegergo02/viscord"
license=('GPL')
depends=('python' 'python-aiohttp' 'python-async-timeout' 'python-attrs' 'python-chardet' 'python-idna' 'python-multidict' 'python-websockets' 'python-yarl' 'python-discord')
makedepends=('git')
source=('git+https://github.com/thegergo02/viscord.git')
md5sums=('SKIP')

pkgver() {
	cd "${_pkgname}"

	printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"

}

prepare() {
    cd "${_pkgname}"
    sed -i '1i#!/usr/bin/env python3' main.py
}

package() {
    install -d $pkgdir/{/opt,/usr/bin}
    cp -a $_pkgname/. "$pkgdir"/opt/$pkgname
    chmod 755 "$pkgdir/opt/$pkgname/main.py"
    
    rm "$pkgdir"/opt/$pkgname/requirements.txt
    rm "$pkgdir"/opt/$pkgname/.gitignore
    rm -rf "$pkgdir"/opt/$pkgname/.github
    rm -rf "$pkgdir"/opt/$pkgname/.git
    
    ln -s /opt/$pkgname/main.py "$pkgdir"/usr/bin/viscord

}
