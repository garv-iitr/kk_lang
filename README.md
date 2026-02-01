# Khel Khatam Language

We are basically making a **transpiler** in which we convert our own language to a **C++ file** to compile it.

## Usage

1. Clone the repository
```bash
git clone https://github.com/garv-iitr/kk_lang.git
```
2. Run
```bash
./run_ide.sh
```
3. Open localhost
```bash
http://localhost:5000
```


## Documentation

### START and END -> `khel_shuru` and `khel_khatam`

The keyword `khel_shuru` is equivalent to 
```cpp
#include <iostream>
using namespace std;

int main(){
```
The keyword `khel_khatam` is equivalent to 
```cpp
    return 0;
}
```
Syntax:
```
khel_shuru

khel_khatam
```


### PRINT -> `aelaan_karo`
The keyword `aelaan_karo` is equivalent to 
```cpp
cout << (expression) << endl;
```

Syntax:
```
khel_shuru
    aelaan_karo ("Hello World");
    aelaan_karo (10);
khel_khatam
```
> [!NOTE]
> **Brackets** are a must

### VAR_DECL -> `khiladi`
`khiladi` is a keyword which is used to declare a type of vairiable in runtime
`khiladi` loosely relates to `auto` in cpp

Syntax:
```
khel_shuru
    khiladi x = 10;
    aelaan_karo (x);
    
    khiladi y = "Hello";
khel_khatam
```
> [!NOTE]
> **Initilization** at the time of declaration is necessary


### ASSIGNMENT 
The syntax of assignment after an operation is exactly same as of cpp
for example 
```
x=x+10;
``` 
is used in cpp as well as kkl (khel khatam lang)

Syntax:
```
khel_shuru
    khiladi x = 10;
    x = x + 1;

khel_khatam
```

### IF-ELSE -> `faisla` and `nahi_toh` 

The syntax of `faisla` and `nahi_toh` is exactly same as of if-else in `cpp`

Syntax:
```
khel_shuru
    khiladi x = 3;
    khiladi y = 1;
    faisla (x==y){
        aelaan_karo (“Are Equal”)
    }
    nahi_toh {
        aelaan_karo (“Not Equal”)
    }
khel_khatam
```
> [!NOTE]
> **Brackets** for the expressions are a must

### WHILE -> `khelte_raho`

Syntax, yet again, matches with `cpp` completely

Syntax:
```
khel_shuru
    khiladi counter = 1;

    khelte_raho (counter <= 5) {
        aelaan_karo("Round number:");
        aelaan_karo(counter);
        counter = counter + 1;
    }
khel_khatam
```




## Process

### 1. Lexing
In this step we have made tokens of each word. We had already created a grammar of our language in which we created tokens.  
Now we traverse through the code and assign tokens to each word and store both of them in a list.


### 2. Parsing
This is the most complex and important step for our project.  
In this we create an **Abstract Syntax Tree (AST)** which store the node of all the steps. This AST helps us in keeping tracks of branching.  
The AST structure is very complex.


### 3. Transpiler
From the AST obtained from the previous step, we make the code to be written in a **C++ file** by traversing this list and creating functions for each process eg. Print, assignment, variable declare etc.  
At the end we receive a cpp file of this.


## Workflow of the AST

So AST, originally a tree is defined I defined as a **nested lists of lists** in the code.  
Initially, starts with the root node. Every new list represents a new branch in the original tree.  
For what we have implemented till now, the branching can only occur at **if condition and the root node**.



## Example Code

### Khel Khatam Code
```
khel_shuru
khiladi x = 10;
aelaan_karo (x);
x = x + 1;
khel_khatam
```




## AST Representation

```bash
[(Token(“START”), 'khel_shuru'), [(Token(“VAR_DECL”), 'khiladi'), [(Token(“ID”), 'x'), (Token(“NUMBER”),'10')]],[(Token(“PRINT”),'aelaan_karo'), (Token(“EXPRESSION”), '(x)')], [(Token(“ASSIGN”), '='), [(Token(“ID”), 'x'), [(Token(“PLUS”), '+'), [(Token(“ID”), 'x'), (Token(“NUMBER”), '1')]]]]]
```


All these token are originally tuple which contains 2 values but only the token is shown here.



## AST Node Structures

### Print Statement

```
[(Token("PRINT"), 'aelaan_karo'), [Token("ID"), '(x)']]
```


### Variable Declaration
```
[(Token("VAR_DECL"), 'khiladi'), [(Token("ID"), 'x'), (Token("NUMBER"), '10')]]
```


### Assignment
```
[(Token("ASSIGN"), '='), [(Token("ID"), 'x'), [(Token("PLUS"), '+'), [(Token("ID"), 'x'), (Token("NUMBER"), '1')]]]]
```

### If Else Statement
```
[(Token("IF"), "faisla"), [(Token("EXPRESSION"), '(x==10)')], [(Token("TRUE"), <Statements>)], [(Token("FALSE"), <Statements>)]]
```


### While Statement
```
[(Token("WHILE"), "khelte_raho"), [(Token("EXPRESSION"), "(n<10)")], [<statements>]]
```


These are the list created.




For implementation purposes, we built a **Flask-based compiler server** that safely executes **"KhelKhatam"** code by transpiling it to **C++**, compiling it with **g++**, and running it inside a **Docker container**.


## Key Components Implemented

### 1. Server (app.py)
- **API Endpoint:** Created a `/compile` endpoint that accepts `.txt` code.
- **Sandboxing:** It spins up a Docker container (`khelkhatam-runner`) for every request to isolate user code execution.
- **Security & Stability:** Implemented `flask_limiter` (50 requests/min) and error handling for timeouts (10s limit) and compilation failures.
- **CORS:** Manually handled CORS headers to allow the frontend to communicate with the server.

### 2. AST (Abstract Syntax Tree) Implementation
- **Purpose:** Implemented an AST to represent the logical structure of the source code after parsing.
- **Structure:** The AST is represented as nested lists, where each list corresponds to a node or a branch in the syntax tree.
- **Branching Support:** Handles control flow constructs such as `if-else`, `while`, and nested loops



## Challenges Faced

1. We thought about how to create the AST on our own so that we really challenging.
2. Nesting of loops was very difficult to implement. As managing the pointer while nesting is difficult.
3. CORS (Cross-Origin Resource Sharing)
- **Issue:** Browsers block requests from one **Origin** (e.g., frontend on port `8000`) to another (backend on port `5000`) for security reasons. Even with `flask-cors`, we faced persistent preflight errors.

- **Fix:** We moved to a **Single Origin Architecture**. Instead of running two separate servers, we configured Flask (`app.py`) to serve the HTML/JS static files itself. Now, everything lives on localhost:5000, so "Cross-Origin" rules no longer apply.




## What Our Code Does

1. It can print.
2. We can declare and store a value of variable.
3. We can assign a value to a variable.
4. We can use loops and nested loops.
5. We can use while loop in this.
6. We have color-coded the Editor which also has auto-recommendation.


## What Our Code Cannot Do

It cannot do all the things that are not mentioned above.