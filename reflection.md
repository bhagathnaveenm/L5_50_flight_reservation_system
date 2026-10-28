1. What static analysis did you learn from this lab?
   I learned that static analysis tools can catch both security and maintainability issues before runtime. Pylint helped highlight naming and structure problems, Flake8 enforced formatting and readability, and Bandit identified vulnerable patterns such as `eval()`, weak hashing, and shell execution.

2. Which issue was most important to fix, and why?
   The most important issue was the unsafe use of `eval()` in the baggage surcharge calculation. It could allow arbitrary code execution if attacker-controlled input reached the expression, so removing it was critical for both security and correctness.

3. How did the fixes improve the code quality?
   The code is now safer and easier to maintain: the default list bug was corrected, invalid flight handling is explicit, manifest export avoids shell injection, and hashing uses a secure algorithm. The functions are also more readable and follow consistent Python conventions.

4. Would you use static analysis in future projects?
   Yes. Static checks are a fast, low-cost way to find defects early in development. In a real project, running these tools regularly would reduce debugging time, improve security, and keep the codebase consistent as it grows.
