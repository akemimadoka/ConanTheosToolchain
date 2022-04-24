from conans import ConanFile, tools
import os
import re

class ConanTheosToolchain(ConanFile):
    name = "TheosToolchain"
    version = "0.1"
    settings = {"os_build": ["Linux"],
                "arch_build": ["x86", "x86_64"],
                "compiler": {"clang": {"libcxx": "libc++"}},
                "os": ["iOS"],
                "arch": ["armv7", "armv8", "armv8.3"]}
    options = {"theos_path": "ANY", "sdk": "ANY"}
    default_options = {"theos_path": None, "sdk": "latest"}
    exports_sources = "theos.toolchain.cmake"

    @property
    def theos_path(self):
        return str(self.options.theos_path or os.environ["THEOS"])

    @property
    def target_cpu(self):
        return {
            "armv7": "armv7",
            "armv8": "arm64",
            "armv8.3": "arm64e",
        }.get(str(self.settings.arch))

    def find_latest_sdk(self):
        sdkPath = os.path.join(self.theos_path, "sdks")
        sdks = [[int(v) for v in re.findall(r"(\d+)", sdk)] for sdk in os.listdir(sdkPath) if sdk.startswith("iPhoneOS")]
        return max(sdks)

    def package(self):
        self.copy("theos.toolchain.cmake")

    def package_info(self):
        theosPath = self.theos_path
        usingSdk = ".".join(map(str, self.find_latest_sdk())) if self.options.sdk == "latest" else str(self.options.sdk)
        sysroot = f"{theosPath}/sdks/iPhoneOS{usingSdk}.sdk"
        deploymentFlags = tools.apple_deployment_target_flag(self.settings.os, self.settings.os.version)
        cflags = [f"-isysroot", sysroot, deploymentFlags, "-arch", self.target_cpu, "-stdlib=libc++"]
        cxxflags = cflags
        linkflags = cflags

        self.cpp_info.cflags = cflags
        self.cpp_info.cxxflags = cxxflags
        self.cpp_info.sharedlinkflags.extend(linkflags)
        self.cpp_info.exelinkflags.extend(linkflags)

        cflagsStr = " ".join(cflags)
        cxxflagsStr = " ".join(cxxflags)
        linkflagsStr = " ".join(linkflags)

        self.env_info.CC = f"{theosPath}/toolchain/linux/iphone/bin/clang"
        self.env_info.CPP = f"{theosPath}/toolchain/linux/iphone/bin/clang -E"
        self.env_info.CXX = f"{theosPath}/toolchain/linux/iphone/bin/clang++"
        self.env_info.AR = f"{theosPath}/toolchain/linux/iphone/bin/ar"
        self.env_info.RANLIB = f"{theosPath}/toolchain/linux/iphone/bin/ranlib"
        self.env_info.STRIP = f"{theosPath}/toolchain/linux/iphone/bin/strip"

        self.env_info.CFLAGS = cflagsStr
        self.env_info.CPPFLAGS = cflagsStr
        self.env_info.ASFLAGS = cflagsStr
        self.env_info.CXXFLAGS = cxxflagsStr
        self.env_info.LDFLAGS = linkflagsStr

        self.env_info.THEOS = self.theos_path
        self.env_info.CONAN_THEOS_TARGET_ARCH = self.target_cpu
        self.env_info.CONAN_THEOS_TARGET_SDK_ROOT = sysroot
        self.env_info.CONAN_THEOS_TARGET_OS_VERSION = str(self.settings.os.version)
        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = os.path.join(self.package_folder, "theos.toolchain.cmake")
