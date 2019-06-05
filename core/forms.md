# Forms
## Problem with action forms
Action form - czyli sytuacja kiedy chce rozdzielic update
na stronie - akcje nie sa w jednej formie.
1. Separate Post View(same for all) and Form(same for all)  - jesli mam jedna forme to reszta fieldow bedzie None
2. Separate Post Views and Forms - duzo duplicates
3. Single Form and Same View - sa pomoca JS i hidden form ktore ma wszystkie fieldy i je wypelnia.