include(default)

[settings]
os=iOS
os.version=7.0
arch=armv8
compiler=clang
compiler.version=10
compiler.libcxx=libc++

[options]
TheosToolchain:sdk=latest

[build_requires]
TheosToolchain/0.1

[env]
