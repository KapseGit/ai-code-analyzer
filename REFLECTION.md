I approached this project as a \*\*legacy modernization problem\*\*, not a coding exercise.



Instead of starting with tools, I started with a business question:



"How would AI safely modernize a financial system if it doesn't understand where revenue, tax and validation logic lives?"



The ERPNext Sales Invoice module was selected because it represents the \*\*financial backbone of an organization\*\*. For this reason, any mistake there could result in the loss of revenue, compliance failure, or accounting inconsistency. I aimed to solve this by providing a system that automatically transformed uncommented Python code into \*\*machine-readable business knowledge\*\* that AI systems can reason about before making edits.



What did I make?



I developed, using Python AST, a \*\*static code intelligence engine\*\* which automatically extracts:

Functions and business rules

\- Classes and inheritance



\- Dependencies among modules

This produces:

\- A \*\*knowledge base for AI entities.json



\- A \*\*human-readable architecture summary - A \*\*Dependency Graph for Risk and Impact Analysis This converts ERPNext from a bunch of files into a \*\*governable, analyzable business system\*\*.





What was difficult?

It was challenging for me to handle \*\*actual enterprise complexity\*\*:

\- Inheritance chains

\- Deep import hierarchies

\- Nested Logic and Hidden Business Rules



Keyword searching and text parsing will not work for the enterprise code.

To extract structure safely and ensure that what I extracted was \*correct, complete, and reliable\*, I \*\*applied AST-based parsing\*\*



What would I do next?



The next step would be to connect this knowledge base to an \*\*LLM using GraphRAG\*\*, so AI could answer questions like

\- What is the logic for invoice totals?

\- “What breaks if I change discount rules?”



\- "Which modules depend on customer credit limits?"



This would allow for \*\*safe, AI-driven refactoring and migration.



---



What are the remaining questions?

How would you merge the following:

\- Static code analysis



Runtime logs



Business documentation into a single \*\*enterprise knowledge model\*\* that AI can reason over. This is where AI can definitely change the dynamics of how legacy systems are modernized.

