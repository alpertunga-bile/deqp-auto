import argparse
from asyncio.subprocess import PIPE
from distutils.command import build
import os
from os.path import exists
from re import A
import subprocess
from subprocess import DEVNULL, STDOUT
import pandas as pd
# --------------------------------------------------------------------------------------------------------------------------------------------
# BEGIN : Parser Configurations

mParser = argparse.ArgumentParser(prog="dEQP-auto",
description="Download, Build and Use dEQP's Vulkan CTS on Windows",
allow_abbrev=False)

mParser.add_argument('--download', '-D', action="store_true", help="Download dEQP from github using git")

mParser.add_argument('--download_location', '--dLocation', '-dL', action="store", type=str, help="Download location to where to download dEQP repository")

mParser.add_argument('--build', '-B', action="store_true", help="Build the dEQP file")

mParser.add_argument('--generator', '-G', action="store", type=str, help="Generator to build dEQP repository, Write in double/single quotes")

mParser.add_argument("--config", action="store", type=str, help="Configure as Release or Debug")

mParser.add_argument("--run", "-R", action="store_true", help="Run Vulkan CTS tests from given file")

mParser.add_argument('--test_file', '-TF', action="store", type=str, help="Run on given tests with file")

mParser.add_argument("--source_file", '-SF', action="store", type=str, help="Store CSV file in given file")

mParser.add_argument("--get_results", action="store_true", help="Get Results From Result.csv or from specified source_file")

args = mParser.parse_args()

# END : Parser Configurations

# --------------------------------------------------------------------------------------------------------------------------------------------
# BEGIN : Initialize with Default variable

mainDirectory = os.getcwd()
dEQPDirectory = os.path.join(os.getcwd(), "dEQP")

if args.build:
    process = subprocess.Popen("cmake --version", stdout=subprocess.PIPE)
    streamdata = process.communicate()[0]

    if process.returncode != 0:
        print("---------------------------------------------------------------------------------------------------------------------")
        print("There is no CMake on your computer or not included in PATH variable, please install it or add to PATH variable and try again")
        exit(1)
    else:
        print("---------------------------------------------------------------------------------------------------------------------")
        print("CMake %10s" % ("FOUND"))

if args.download:
    process = subprocess.Popen("git --version", stdout=subprocess.PIPE)
    streamdata = process.communicate()[0]

    if process.returncode != 0:
        print("---------------------------------------------------------------------------------------------------------------------")
        print("There is no Git on your computer or not included in PATH variable, please install it or add to PATH variable and try again")
        exit(1)
    else:
        print("---------------------------------------------------------------------------------------------------------------------")
        print("Git %12s" % ("FOUND"))

if args.generator is None:
    args.generator = '"Visual Studio 17 2022"'
    if args.build:
        print("---------------------------------------------------------------------------------------------------------------------")
        print(f"Generator specified as {args.generator}")
        print("You can look https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html for generators that CMake use")

if args.config is None:
    args.config = "Release"
    if args.build:
        print("---------------------------------------------------------------------------------------------------------------------")
        print("Config specified as Release")

if args.run and args.test_file is None:
    print("---------------------------------------------------------------------------------------------------------------------")
    args.test_file = mainDirectory + "\\mandatory.txt"
    print(f"Test file selected as {args.test_file}")

if args.download_location is None:
    if args.download:
        print("---------------------------------------------------------------------------------------------------------------------")
        print(f"dEQP folder selected as {dEQPDirectory}")
    if not exists(dEQPDirectory):
        os.mkdir(dEQPDirectory)
else:
    dEQPDirectory = args.download_location

if args.source_file is None:
    args.source_file = mainDirectory + "\\Result.csv"
    if args.run:
        print("---------------------------------------------------------------------------------------------------------------------")
        print(f"Result is going to write in {args.source_file}")

# END : Initialize with Default variable

# --------------------------------------------------------------------------------------------------------------------------------------------
# BEGIN : dEQP-auto Functions

if args.download:
    print("---------------------------------------------------------------------------------------------------------------------")
    print("Downloading Started")
    print("|    %s" % ("Entering " + dEQPDirectory))
    os.chdir(dEQPDirectory)
    print("|    %s" % ("Downloading Vulkan CTS from Github"))
    retcode = subprocess.check_call("git clone https://github.com/KhronosGroup/VK-GL-CTS", stdout=DEVNULL, stderr=STDOUT)
    print("Downloading Finished")

if args.build:
    print("---------------------------------------------------------------------------------------------------------------------")
    print("Building Started")
    os.chdir(os.path.join(dEQPDirectory, "VK-GL-CTS\\external"))
    print("|    %s" % ("Downloading required python libraries"))
    #retcode = subprocess.check_call("python fetch_sources.py", stdout=DEVNULL, stderr=STDOUT)
    os.chdir(dEQPDirectory)
    print("|    %s" % ("Building..."))
    retcode = subprocess.check_call("cmake " + os.path.join(dEQPDirectory, "VK-GL-CTS\\") + " -G " + args.generator + " -B" + os.path.join(dEQPDirectory, "VK-GL-CTS\\build"), stdout=DEVNULL, stderr=STDOUT)
    print("|    %s" % ("Building deqp-vk"))
    retcode = subprocess.check_call("cmake --build " + dEQPDirectory + "\\VK-GL-CTS\\build" + " --config " + args.config + " --target deqp-vk", stdout=DEVNULL, stderr=STDOUT)
    print("|    %s" % ("Building testlog-to-csv"))
    retcode = subprocess.check_call("cmake --build " + dEQPDirectory + "\\VK-GL-CTS\\build" + " --config " + args.config + " --target testlog-to-csv", stdout=DEVNULL, stderr=STDOUT)
    print("Building Finished")

if args.run:
    print("---------------------------------------------------------------------------------------------------------------------")
    print("Run&Save Started")
    os.chdir(dEQPDirectory + "\\VK-GL-CTS\\build\\external\\vulkancts\\modules\\vulkan")
    print("|    Testing...")
    retcode = subprocess.call(args.config + "\\deqp-vk.exe --deqp-caselist-file=" + args.test_file + " --deqp-log-images=disable --deqp-log-shader-sources=disable")
    os.chdir(dEQPDirectory + "\\VK-GL-CTS\\build\\executor\\" + args.config)
    print("|    Saving to " + args.source_file)
    os.system("testlog-to-csv.exe --value=code " + dEQPDirectory + "\\VK-GL-CTS\\build\\external\\vulkancts\\modules\\vulkan\\TestResults.qpa > " + args.source_file)
    print("Run&Save Finished")

if args.get_results:
    print("---------------------------------------------------------------------------------------------------------------------")
    data = pd.read_csv(args.source_file)
    print(data)

# END : dEQP-auto Functions