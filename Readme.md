ConanTheosToolchain
====

![License](https://img.shields.io/badge/license-MIT-blue.svg)

提供 toolchain 支持，使得 conan 可以生成 theos 目标的依赖

安装
----

```bash
conan config install -tf profiles theos.profile
```

使用
----

假定正在使用 conanfile.txt 描述依赖，并使用 build 文件夹放置生成的文件

```bash
conan install conanfile.txt -pr theos.profile -if build --build missing
```

之后在 Makefile 中添加（假定 MyProject 是你的工程名）

```Makefile
include build/conanbuildinfo.mak

MyProject_CCFLAGS += $(CONAN_CXXFLAGS)
MyProject_CCFLAGS += $(addprefix -I, $(CONAN_INCLUDE_DIRS))
MyProject_CCFLAGS += $(addprefix -D, $(CONAN_DEFINES))
MyProject_LDFLAGS += $(addprefix -L, $(CONAN_LIB_DIRS))
MyProject_LDFLAGS += $(addprefix -l, $(CONAN_LIBS))
```

注意
----

若使用 [官方推荐的带 Swift 支持的工具链](https://github.com/CRKatri/llvm-project)，需要在 toolchain/linux/iphone/bin 下执行以下命令

```bash
ln -s ranlib aarch64-apple-darwin-ranlib
```

否则会出现 internal ranlib command failed 的问题
