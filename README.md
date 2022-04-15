# deqp-auto

Download, Build and Use dEQP's [Vulkan CTS](https://github.com/KhronosGroup/VK-GL-CTS) on Windows

## Full auto

You must have Visual Studio 17 2022 for this command<br/>

```python deqp-auto.py --download --build --run --get_results``` <br/>

## Download

LOCATION : CSV file location. Ex. Result.csv <br/>

```python deqp-auto.py --download --download_location [LOCATION]``` <br/>

## Build

GENERATOR : Solution generator. Ex. "Visual Studio 17 2022" <br/>
  You can look generators from [this](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html) <br/>
  Write generator name between double quotes <br/>
CONFIG    : Release or Debug <br/>

```python deqp-auto.py --build -G [GENERATOR] --config [CONFIG]``` <br/>

## Run Tests

CASETEST_FILE : Required tests file. Ex. mandatory.txt <br/>
SOURCE_FILE   : Write CSV file to given location <br/>

```python deqp-auto.py --run --test_file [CASETEST_FILE] --source_file [SOURCE_FILE]``` <br/>

## Get Results From CSV

```python deqp-auto.py --get_results --source_file [SOURCE_FILE]``` <br/>




