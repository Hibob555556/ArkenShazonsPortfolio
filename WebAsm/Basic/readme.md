# Web Assembly Project

## Setting up the project

1) Install the emsdk package

- ```bash
    git clone https://github.com/emscripten-core/emsdk.git 
  ```

2) Navigate to the emsdk directory

- ```bash
    cd emsdk
  ```

3) Install and activate the latest version of emsdk

- ```bash
    ./emsdk install latest 
    ./emsdk activate latest
  ```

4) Compile the project using emcc

- ```bash
    emcc main.c -O3 -s WASM=1 -s EXPORTED_FUNCTIONS='["_add", "_mult", "_fib"]' -s EXPORTED_RUNTIME_METHODS='["cwrap", "HEAP32"]' -o main.js
  ```

5) Start a simple python server to view your project

- ```bash
    python -m http.server
  ```

6) In a browser of your choice navigate to http://localhost:8000 to see the program
