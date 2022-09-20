<!--
parent:
  order: false
-->

<div align="center">
  <h1> Hailstone Repo(savour backend service) </h1>
</div>

<div align="center">
  <a href="https://github.com/SavourDao/hailstone/releases/latest">
    <img alt="Version" src="https://img.shields.io/github/tag/SavourDao/savour-core.svg" />
  </a>
  <a href="https://github.com/SavourDao/hailstone/blob/main/LICENSE">
    <img alt="License: Apache-2.0" src="https://img.shields.io/github/license/SavourDao/savour-core.svg" />
  </a>
   <a href="https://www.python.org/downloads/">
    <img alt="License: Apache-2.0" src="http://img.shields.io/badge/Python3.*-ff3366.svg"/>
  </a>
  
 
</div>

This project is written in python Django, the dependency version is above python3, python3.8.* is recommended

## Project deployment

### 1.install dependencies

`pip3 install -r requirements.txt`

### 2.migrate database

`python3 manager migrations`

### 3. run dev

`python3 manager runserver`

